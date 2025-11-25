import pygame
from .entity import Entity

class BasicZombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, image_path, strength = 50, max_hp = 305, attack_range = 1, attack_speed = 500, move_speed = 1)

    def animate(self, dt):
        # 구현 필요함
        pass

    def attack(self, plant):
        now = pygame.time.get_ticks()
        # 공격 범위 내에 있다면
        if (now - self.last_attack_time > self.attack_speed) and (self.x - plant.x < self.attack_range):
            self.last_attack_time = now
            plant.take_damage(self.strength) # 식물에게 공격력만큼 데미지