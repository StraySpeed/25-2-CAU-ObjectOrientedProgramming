import pygame
from .entity import Entity
from .sun import Sun
from .bullet import Bullet
from ..loader.imageLoader import ImageLoader
from ..const import * # 필요 시 import

class Peashooter(Entity):
    def __init__(self, x, y, idle_image):
        # ImageLoader에서 받아온 image를 그대로 Entity에게 전달
        super().__init__(
            x, y, 
            image=idle_image, 
            strength=50, 
            max_hp=300, 
            attack_range=idle_image.get_size()[0] * 9,    # 9칸 범위를 공격 가능하게 
            attack_speed=2000, 
            move_speed=0
        )
        self.idle_image = idle_image

        self.bullet_loader = ImageLoader(BULLET_SPRITE, BULLET_BROKEN_SPRITE)
        for i in range(len(self.bullet_loader.images)): self.bullet_loader.resize(i, *(s / 2 for s in self.idle_image.get_size()))
        self.idle_bullet = self.bullet_loader.getSprite(0)
        self.broken_bullet = self.bullet_loader.getSprite(1)
    
    def animate(self, dt):
        return
        if self.isAttack():
            self.image = self.attack_image
        else:
            self.image = self.idle_image  

        # 보류
    '''def zombie_is_same_row(self, zombies):
        for zombie in zombies:
            if (abs(self.rect.centery - zombie.rect.centery) < 10) and abs(self.rect.centerx - zombie.rect.centrx) < self.attack_range: # 같은 행에 있는지 체크
                self.attack()
                return True
        return False'''

    def isAttack(self):
        if self.attack():
            return True
        else: False    

    def attack(self, zombies_group):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time < self.attack_speed:
            return None

        # 사거리 내 좀비 체크
        can_fire = False
        for zombie in zombies_group:
            # 같은 줄에 있는지 확인
            if abs(zombie.rect.centery - self.rect.centery) == 0:
                
                # 좀비가 식물보다 오른쪽에 있는지
                # 좀비가 사거리(attack_range) 안에 있는지
                distance = zombie.rect.centerx - self.rect.centerx
                if 0 < distance <= self.attack_range:
                    can_fire = True
                    break # 쏠 좀비를 하나라도 찾았으면 루프 종료

        if can_fire:
            self.last_attack_time = now
            bullet = Bullet(self.position.x, self.position.y, self.idle_bullet, self.broken_bullet, self.strength, "Peashooter(" + self.name + ")", self.attack_range) # 총알 생성
            print(f"[DEBUG] Peashooter({self.name}) shooted Bullet({bullet.name}).")
            return bullet 
        return False
    
class SunFlower(Entity):
    def __init__(self, x, y, image):
        super().__init__(
            x, y, 
            image=image,
            strength = 0, 
            max_hp = 300, 
            attack_range = 10, 
            attack_speed = 5000, 
            move_speed = 0
        )
        self.sun_loader = ImageLoader(SUN_SPRITE)
        self.sun_loader.resize(0, *(s / 2 for s in self.image.get_size()))
        self.sun_image = self.sun_loader.getSprite(0)

    def obtain_sun(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_speed: #해바라기 기준 공격 = 햇빛 획득
            self.last_attack_time = now
            # 살짝 우측 위로 태양을 생성하기
            return Sun(self.position.x + self.image.get_size()[0] / 2, self.position.y - self.image.get_size()[1] / 2, self.sun_image)
        return False
    

    def attack(self, zombies_group):
        pass

    def animate(self, dt):
        pass

class WallNut(Entity):
    def __init__(self, x, y, image):
        super().__init__(
            x, y, 
            image = image, 
            strength = 0,
            max_hp = 1000, 
            attack_range = 0, 
            attack_speed = 0, 
            move_speed = 0
        )

    def isAttack(self):
        if self.attack():
            return True
        else: False

    def attack(self, zombies_group):
        pass

    def animate(self, dt):
        pass