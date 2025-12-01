import pygame
from .stateManager import StateManager
from .gameManager import GameManager
from .fontLoader import FontLoader
from ..const import *

class Button:
    """
    버튼 클래스

    :param rect: 생성할 위치
    :param text: 입력 텍스트
    :param font: 적용 폰트
    :param action: event (기본 None)
    """
    def __init__(self, rect, text, font, action=None):
        self.rect = rect
        self.text = text
        self.action = action
        self.font = font
        self.default_color = DEFAULT_COLOR
        self.hover_color = HOVER_COLOR
        self.text_color = TEXT_COLOR

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.default_color
        
        # 버튼 그리기
        # 배경 채우기
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        # 테두리 그리기
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        # 텍스트 그리기
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

class UIManager:
    _instance = None # 싱글톤 인스턴스

    def __new__(cls, *args, **kwargs):
        """싱글톤 패턴"""
        if not cls._instance:
            cls._instance = super(UIManager, cls).__new__(cls)
            # 초기화 여부 플래그 (중복 init 방지)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, screen_width=800, screen_height=600):
        # 이미 초기화되었다면 건너뜀
        if self.initialized:
            return
        
        self.width = screen_width
        self.height = screen_height
        self.initialized = True
        self.state_mgr = StateManager()

        # 배경 설정
        self._load_background()

        # 폰트 설정
        self.title_font = FontLoader.load_font(int(self.height * 0.13))
        self.guide_font = FontLoader.load_font(int(self.height * 0.08))
        self.btn_font = FontLoader.load_font(int(self.height * 0.05))

        # 반투명 오버레이 (일시정지/게임오버 배경용)
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(150) # 반투명하게
        self.overlay.fill(BLACK) # 검은색

        # 버튼 생성
        self._create_menu_buttons()
        self._create_level_buttons()
        self._create_pause_buttons()
        self._create_result_buttons()

    def _load_background(self):
        """
        배경 로드하기
        """
        try:
            bg_img = pygame.image.load(MAIN_BACKGROUND_IMAGE).convert()
            self.main_background = pygame.transform.scale(bg_img, (self.width, self.height))
        except FileNotFoundError:
            self.main_background = None
            print(f"[DEBUG] Cannot find {MAIN_BACKGROUND_IMAGE}.")

        try:
            bg_img = pygame.image.load(SELECT_LEVEL_BACKGROUND_IMAGE).convert()
            self.select_level_background = pygame.transform.scale(bg_img, (self.width, self.height))
        except FileNotFoundError:
            self.select_level_background = None
            print(f"[DEBUG] Cannot find {SELECT_LEVEL_BACKGROUND_IMAGE}.")

        try:
            bg_img = pygame.image.load(LEVEL1_BACKGROUND_IMAGE).convert()
            self.level1_background = pygame.transform.scale(bg_img, (self.width, self.height))
        except FileNotFoundError:
            self.level1_background = None
            print(f"[DEBUG] Cannot find {LEVEL1_BACKGROUND_IMAGE}.")

        try:
            bg_img = pygame.image.load(LEVEL2_BACKGROUND_IMAGE).convert()
            self.level2_background = pygame.transform.scale(bg_img, (self.width, self.height))
        except FileNotFoundError:
            self.level2_background = None
            print(f"[DEBUG] Cannot find {LEVEL2_BACKGROUND_IMAGE}.")

        try:
            bg_img = pygame.image.load(LEVEL3_BACKGROUND_IMAGE).convert()
            self.level3_background = pygame.transform.scale(bg_img, (self.width, self.height))
        except FileNotFoundError:
            self.level3_background = None
            print(f"[DEBUG] Cannot find {LEVEL3_BACKGROUND_IMAGE}.")

    def calc_center_rect(self, cx_ratio, cy_ratio, w_ratio, h_ratio):
        """
        중심점(cx, cy)을 기준으로 Rect를 계산

        :param cx_ratio: 화면 너비 대비 x 위치
        :param cy_ratio: 화면 높이 대비 y 위치
        :param w_ratio: 화면 너비 대비 버튼 폭
        :param h_ratio: 화면 높이 대비 버튼 높이
        :return: Rect object
        """
        w = int(self.width * w_ratio)
        h = int(self.height * h_ratio)
        x = int(self.width * cx_ratio) - (w // 2)
        y = int(self.height * cy_ratio) - (h // 2)
        return pygame.Rect(x, y, w, h)

    def _create_menu_buttons(self):
        """
        메뉴 버튼 생성
        """
        # 가로 중앙(0.5), 세로 35% 지점에 너비 25%, 높이 10% 버튼
        rect_play = self.calc_center_rect(0.5, 0.4, 0.25, 0.1)
        rect_quit = self.calc_center_rect(0.5, 0.55, 0.25, 0.1)

        btn_play = Button(rect_play, "Game Play", self.btn_font,
                          lambda: self.state_mgr.change_state(STATE_LEVEL_SELECT))
        
        btn_quit = Button(rect_quit, "Quit", self.btn_font,
                          lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        
        self.menu_buttons = [btn_play, btn_quit]

    def _create_level_buttons(self):
        """
        레벨 버튼 생성
        """
        def start_lvl(n):
            return lambda: self.state_mgr.start_game(n, GameManager, self.width, self.height)

        # 레벨 버튼: 너비 25%, 높이 8%로 설정
        # y위치를 25%, 35%, 45% ... 로 배치
        btn_w, btn_h = 0.25, 0.08
        
        rect_l1 = self.calc_center_rect(0.5, 0.30, btn_w, btn_h)
        rect_l2 = self.calc_center_rect(0.5, 0.40, btn_w, btn_h)
        rect_l3 = self.calc_center_rect(0.5, 0.50, btn_w, btn_h)
        rect_back = self.calc_center_rect(0.5, 0.65, btn_w, btn_h)

        self.level_buttons = [
            Button(rect_l1, "Level 1", self.btn_font, start_lvl(1)),
            Button(rect_l2, "Level 2", self.btn_font, start_lvl(2)),
            Button(rect_l3, "Level 3", self.btn_font, start_lvl(3)),
            Button(rect_back, "Back", self.btn_font, lambda: self.state_mgr.change_state(STATE_MENU))
        ]

    def _create_pause_buttons(self):
        """
        일시정지 화면 버튼들
        """
        btn_w, btn_h = 0.25, 0.08
        
        # Resume: 다시 게임으로
        btn_resume = Button(self.calc_center_rect(0.5, 0.4, btn_w, btn_h), "Resume", self.btn_font,
                            lambda: self.state_mgr.change_state(STATE_GAME))
        
        # Restart: 현재 레벨 재시작
        btn_restart = Button(self.calc_center_rect(0.5, 0.5, btn_w, btn_h), "Restart", self.btn_font,
                             lambda: self.state_mgr.restart_game(GameManager, self.width, self.height))
        
        # Main Menu: 메뉴로 나가기
        btn_menu = Button(self.calc_center_rect(0.5, 0.6, btn_w, btn_h), "Main Menu", self.btn_font,
                          lambda: self.state_mgr.quit_current_game())

        self.pause_buttons = [btn_resume, btn_restart, btn_menu]

    def _create_result_buttons(self):
        """
        게임 오버/클리어 화면 버튼들
        """
        btn_w, btn_h = 0.25, 0.08
        
        # Restart
        btn_restart = Button(self.calc_center_rect(0.5, 0.55, btn_w, btn_h), "Try Again", self.btn_font,
                             lambda: self.state_mgr.restart_game(GameManager, self.width, self.height))
        
        # Main Menu
        btn_menu = Button(self.calc_center_rect(0.5, 0.65, btn_w, btn_h), "Main Menu", self.btn_font,
                          lambda: self.state_mgr.quit_current_game())
        
        self.result_buttons = [btn_restart, btn_menu]

    def process_events(self, event):
        """
        UI 관련 이벤트 처리
        """
        current_state = self.state_mgr.current_state
        
        if current_state == STATE_MENU:
            for btn in self.menu_buttons: btn.handle_event(event)
        elif current_state == STATE_LEVEL_SELECT:
            for btn in self.level_buttons: btn.handle_event(event)
        elif current_state == STATE_PAUSE:
            for btn in self.pause_buttons: btn.handle_event(event)
        elif current_state == STATE_GAME_OVER or current_state == STATE_GAME_CLEAR:
            for btn in self.result_buttons: btn.handle_event(event)

    def draw(self, screen):
        """
        현재 상태에 따라 화면 그리기
        """
        current_state = self.state_mgr.current_state
        
        # 게임 화면은 PAUSE/OVER/CLEAR 상태에서도 뒤에 깔려 있어야 함
        if current_state in [STATE_GAME, STATE_PAUSE, STATE_GAME_OVER, STATE_GAME_CLEAR]:
            self._draw_game_elements(screen) # 게임 요소 그리기

        # 상태별 UI 그리기
        if current_state == STATE_MENU:
            self._draw_main_menu(screen)

        elif current_state == STATE_LEVEL_SELECT:
            self._draw_level_select(screen)

        elif current_state == STATE_PAUSE:
            self._draw_pause_screen(screen)

        elif current_state == STATE_GAME_OVER:
            self._draw_result_screen(screen, "GAME OVER", (200, 0, 0))

        elif current_state == STATE_GAME_CLEAR:
            self._draw_result_screen(screen, "LEVEL CLEARED!", (0, 200, 0))

    def _draw_main_menu(self, screen):
        """메인 화면"""
        if self.main_background: screen.blit(self.main_background, (0, 0))
        # 제목 위치도 비율로 계산 (중앙 상단 15%)
        title_surf = self.title_font.render("Main Menu", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(self.width * 0.5, self.height * 0.15))
        screen.blit(title_surf, title_rect)
        
        for btn in self.menu_buttons:
            btn.draw(screen)

    def _draw_level_select(self, screen):
        """ 레벨 선택 화면 """
        if self.select_level_background: screen.blit(self.select_level_background, (0, 0))
        guide_surf = self.guide_font.render("Select Level", True, TEXT_COLOR)
        guide_rect = guide_surf.get_rect(center=(self.width * 0.5, self.height * 0.15))
        screen.blit(guide_surf, guide_rect)
        
        for btn in self.level_buttons:
            btn.draw(screen)

    def _draw_game_elements(self, screen):
        """게임 내 객체와 그리드 그리기"""
        if self.state_mgr.current_level_num == 1:
            if self.level1_background: screen.blit(self.level1_background, (0, 0))
        elif self.state_mgr.current_level_num == 2:
            if self.level2_background: screen.blit(self.level2_background, (0, 0))
        elif self.state_mgr.current_level_num == 3:
            if self.level3_background: screen.blit(self.level3_background, (0, 0))

        # 그리드
        for i in range(5):
            y = 100 + (i * 100)
            pygame.draw.line(screen, BLACK, (0, y), (self.width, y))
            pygame.draw.line(screen, BLACK, (0, y+100), (self.width, y+100))

        # 객체
        if self.state_mgr.game_manager:
            self.state_mgr.game_manager.draw(screen)

    def _draw_pause_screen(self, screen):
        """일시정지 화면"""
        screen.blit(self.overlay, (0, 0)) # 반투명 배경
        
        title_surf = self.title_font.render("PAUSED", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.width * 0.5, self.height * 0.25))
        screen.blit(title_surf, title_rect)

        for btn in self.pause_buttons:
            btn.draw(screen)

    def _draw_result_screen(self, screen, text, color):
        """결과 화면 (오버/클리어 공용)"""
        screen.blit(self.overlay, (0, 0)) # 반투명 배경
        
        title_surf = self.title_font.render(text, True, color)
        title_rect = title_surf.get_rect(center=(self.width * 0.5, self.height * 0.3))
        screen.blit(title_surf, title_rect)

        for btn in self.result_buttons:
            btn.draw(screen)