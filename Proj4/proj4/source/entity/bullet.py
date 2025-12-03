import pygame
from ..const import *
from ..loader.imageLoader import ImageLoader
from .entity import Entity

class Bullet(Entity):
    def __init__(self, x, y, idle_image, broken_image, strenght = 25, origin_entity = "", attack_range = 1000):
        
        super().__init__(
            x, y, 
            image=idle_image, 
            strength=strenght, 
            max_hp=1, 
            attack_range=attack_range, 
            attack_speed=0, 
            move_speed=300  # 총알 속도
        )
        self.initial_x = x
        self.idle_image = idle_image
        self.broken_image = broken_image
        self.origin_entity_name = origin_entity

    def update(self, dt):
        # 총알 이동 로직
        self.position.x += self.move_speed * (dt / 1000)  # dt는 밀리초 단위이므로 초 단위로 변환
        self.rect.centerx = round(self.position.x)

        # 화면 밖으로 나가면 제거
        if self.rect.left > pygame.display.get_surface().get_width():
            self.kill()

        # 공격 사거리 벗어나면 없애기
        if self.initial_x + self.attack_range < self.rect.centerx:
            self.kill()

    def attack(self):
        return

    def animate(self, dt):
        return