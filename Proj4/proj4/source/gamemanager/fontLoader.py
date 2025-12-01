from ..const import GAME_FONT
import pygame

class FontLoader:
    @staticmethod
    def load_font(size):
        """
        ## 폰트 로더
        
        :param size: 폰트 크기
        :return: Font object
        """
        try:
            # ttf 파일 로드 시도
            return pygame.font.Font(GAME_FONT, size)
        except (FileNotFoundError, OSError):
            print(f"[DEBUG] Cannot find '{GAME_FONT}'.")
            # 파일이 없으면 시스템 기본 폰트(None) 사용
            return pygame.font.Font(None, size)