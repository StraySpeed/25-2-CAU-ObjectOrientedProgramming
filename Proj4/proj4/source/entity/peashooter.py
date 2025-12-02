import pygame
from .entity import Entity
# from ..const import * # 필요 시 import

class Peashooter(Entity):
    def __init__(self, x, y, image):
        # ImageLoader에서 받아온 image를 그대로 Entity에게 전달
        super().__init__(
            x, y, 
            image=image, 
            strength=50, 
            max_hp=300, 
            attack_range=10, 
            attack_speed=1000, 
            move_speed=0
        )

    def animate(self, dt):
        # 애니메이션 로직 (추후 구현)
        pass

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_speed:
            self.last_attack_time = now
            # 총알 발사 로직 구현 필요
            print(f"[DEBUG] {self.name} Attack") 
            return True 
        return False