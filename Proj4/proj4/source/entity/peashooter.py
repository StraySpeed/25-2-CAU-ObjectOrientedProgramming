import pygame
from .entity import Entity
from .bullet import Bullet
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
    
    def animate(self):
        if self.isAttack():
            self.image = pygame.image.load('assets/peashooter_attack.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/peashooter_idle.png').convert_alpha()    
        pass

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_speed:
            self.last_attack_time = now
            
            Bullet(self.rect.centerx, self.rect.centry) # 총알 생성
            print(f"[DEBUG] {self.name} Attack") 
            return True 
        return False
    
    def isAttack(self):
        if self.attack():
            return True
        else: False