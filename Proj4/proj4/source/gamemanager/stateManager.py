from ..const import *

class StateManager:
    _instance = None # 싱글톤 인스턴스

    def __new__(cls, *args, **kwargs):
        """싱글톤 패턴"""
        if not cls._instance:
            cls._instance = super(StateManager, cls).__new__(cls, *args, **kwargs)
            # 초기화 여부 플래그 (중복 init 방지)
            cls._instance.current_state = STATE_MENU
            cls._instance.game_manager = None # 현재 실행 중인 게임 관리자
        return cls._instance

    def change_state(self, new_state):
        """
        상태 변경
        """
        self.current_state = new_state
        print(f"[DEBUG] State changed to: {self.current_state}")

    def start_game(self, level, game_manager_class, screen_width, screen_height):
        """
        게임을 시작할 때 호출 (GameManager 생성)
        """
        print(f"[DEBUG] Starting Level {level}...")
        
        # 레벨 로드
        self.current_level_num = level # 재시작을 위해 레벨 저장
        
        # 외부에서 받아온 GameManager를 사용하여 인스턴스 생성
        self.game_manager = game_manager_class(screen_width, screen_height, level)
        self.change_state(STATE_GAME)

    def restart_game(self, game_manager_class, width, height):
        """
        현재 레벨 재시작
        """
        self.start_game(self.current_level_num, game_manager_class, width, height)

    def quit_current_game(self):
        """
        메인 메뉴로 돌아가기
        """
        self.game_manager = None
        self.change_state(STATE_MENU)

    def quit_current_game(self):
        """
        게임 중단 후 메뉴로 복귀
        """
        self.game_manager = None
        self.change_state(STATE_MENU)