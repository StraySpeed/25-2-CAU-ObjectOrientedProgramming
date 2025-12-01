import pygame
import sys, json
from .gamemanager.stateManager import StateManager
from .gamemanager.uiManager import UIManager
from .const import *

class Application:
    def __init__(self):
        # Pygame 초기화
        pygame.init()

        # settings.json 가져오기
        with open(SETTINGS, 'r') as f:
            self.data = json.load(f)

        # 기본 설정하기
        self.width = self.data.get('width')
        self.height = self.data.get('height')
        self.fps = self.data.get('fps')
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("OOP Team7 Plants vs Zombies")
        self.clock = pygame.time.Clock()

        # 매니저 초기화
        self.state_mgr = StateManager()
        self.ui_mgr = UIManager(self.width, self.height)
        
        self.running = True

    def run(self):
        """ 메인 게임 루프 """
        while self.running:
            dt = self.clock.tick(self.fps)
            self._handle_events()
            self._update(dt)
            self._draw()
            
        self._quit()

    def _handle_events(self):
        """ 입력 이벤트 처리 """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # UI(버튼) 이벤트 처리
            self.ui_mgr.process_events(event)
            
            # 게임 플레이 중 키 입력 처리
            if self.state_mgr.current_state == STATE_GAME or self.state_mgr.current_state == STATE_PAUSE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current = self.state_mgr.current_state
                    
                    # 게임 중 -> 일시정지
                    if current == STATE_GAME:
                        self.state_mgr.change_state(STATE_PAUSE)
                    
                    # 일시정지 -> 게임 재개
                    elif current == STATE_PAUSE:
                        self.state_mgr.change_state(STATE_GAME)

                # 추후 게임 내 마우스 클릭(식물 배치 등)
                # self.state_mgr.game_manager.handle_input(event)

    def _update(self, dt):
        """ 로직 업데이트 """
        if self.state_mgr.current_state == STATE_GAME:
            if self.state_mgr.game_manager:
                self.state_mgr.game_manager.update(dt)

    def _draw(self):
        """ 화면 그리기 """
        # 그리기 작업은 전적으로 UI Manager에게 위임
        self.ui_mgr.draw(self.screen)
        pygame.display.flip()

    def _quit(self):
        pygame.quit()
        sys.exit()