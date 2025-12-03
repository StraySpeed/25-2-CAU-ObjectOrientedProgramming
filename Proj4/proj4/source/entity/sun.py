import pygame
from ..const import *
class Sun(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.value = SUN_VALUE  # 태양 하나당 25원
        self.spawn_time = pygame.time.get_ticks()
        self.lifespan = 10000 # 10초 뒤 사라짐
        print(f"[DEBUG] Sun created at ({x}, {y}).")

    def update(self, dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.lifespan:
            self.kill()

    def handle_event(self, event):
        """클릭 이벤트 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 좌클릭
                if self.rect.collidepoint(event.pos):
                    return self.value # 수집된 값 반환
        return 0