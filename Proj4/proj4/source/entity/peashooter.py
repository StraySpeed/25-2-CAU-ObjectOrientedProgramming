import pygame
from .entity import Entity
from ..const import *

class Peashooter(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, image_path = TEST_SPRITE, strength = 50, max_hp = 300, attack_range = 10, attack_speed = 1000, move_speed = 0)

    def animate(self, dt):
        # 구현 필요함
        pass

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_speed:
            self.last_attack_time = now
            # attack 로직(총알 발사 등)
            return True # 공격 성공
        return False