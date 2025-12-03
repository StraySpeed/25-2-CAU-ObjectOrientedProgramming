import pygame
from .entity import Entity

class Bullet(Entity):
    def __init__(self, x, y, image):
        
        super().__init__(
            x, y, 
            image=image, 
            strength=25, 
            max_hp=1, 
            attack_range=0, 
            attack_speed=0, 
            move_speed=300  # 총알 속도
        )

    def update(self, dt):
        # 총알 이동 로직
        self.position.x += self.move_speed * (dt / 1000)  # dt는 밀리초 단위이므로 초 단위로 변환
        self.rect.centerx = round(self.position.x)

        # 화면 밖으로 나가면 제거
        if self.rect.left > pygame.display.get_surface().get_width():
            self.kill()