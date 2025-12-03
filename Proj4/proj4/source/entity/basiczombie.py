import pygame
from .entity import Entity
from ..const import *

class BasicZombie(Entity):
    def __init__(self, x, y, image):
        super().__init__(
            x, y, 
            image=image, 
            strength=30, 
            max_hp=200, 
            attack_range=10, 
            attack_speed=500, 
            move_speed=50
        )

    def animate(self, plant):
        # 애니메이션 로직 구현 필요
        if self.isAttack(plant):
            self.image = pygame.image.load('assets/basiczombie_attack.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/basiczombie_walk.png').convert_alpha()
        pass

    def attack(self, plant):
        now = pygame.time.get_ticks()
        # 공격 쿨타임 및 거리 체크
        if now - self.last_attack_time > self.attack_speed:
            self.last_attack_time = now
             # Entity 클래스에 정의된 setDamage 사용
            if hasattr(plant, 'setDamage'):
                plant.setDamage(self.strength) 
                print(f"[DEBUG] Basiczombie({self.name}) attacks plant({plant.name})! Damage: {self.strength}")
            return True
        return False
    
    def isAttack(self, plant):
        if self.attack(plant):
            return True
        else: False

        

class StrongZombie(Entity):
    def __init__(self, x, y, image):
        super().__init__(
            x, y, 
            image=image, 
            strength=50, 
            max_hp=305, 
            attack_range=10, 
            attack_speed=500, 
            move_speed=50
        )
       

    def animate(self, plant):
        # 애니메이션 로직 구현 필요
        if self.isAttack(plant):
            self.image = pygame.image.load('assets/basiczombie_attack.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/basiczombie_walk.png').convert_alpha()
        pass

    def attack(self, plant):
        now = pygame.time.get_ticks()
        # 공격 쿨타임 및 거리 체크
        if now - self.last_attack_time > self.attack_speed:
            self.last_attack_time = now
             # Entity 클래스에 정의된 setDamage 사용
            if hasattr(plant, 'setDamage'):
                plant.setDamage(self.strength) 
                print(f"[DEBUG] Strongzombie({self.name}) attacks plant({plant.name})! Damage: {self.strength}")
            return True
        return False
    
    def isAttack(self, plant):
        if self.attack(plant):
            return True
        else: False
