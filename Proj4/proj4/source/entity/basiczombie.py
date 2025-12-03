import pygame
from .entity import Entity

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

    def animate(self):
        # 애니메이션 로직 구현 필요
        if self.isAttack():
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
    
    def isAttack(self):
        if self.attack():
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
       

    def animate(self, dt):
        # 구현 필요함
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            if self.state == 'dying':
                if(self.current_frame_index <= len(self.animation_frames['dying']) -1):
                    self.current_frame_index += 1
            else: self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames[self.state])

        if self.state == 'dying':
            self.image = self.animation_frames['dying'][self.current_frame_index]
        elif self.state == 'walking':
            self.image = self.animation_frames['walking'][self.current_frame_index]
        elif self.state == 'attacking':
            self.image = self.animation_frames['attacking'][self.current_frame_index]
            #self.attack()
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