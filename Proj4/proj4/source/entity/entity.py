import pygame
import abc

class Entity(pygame.sprite.Sprite, abc.ABC):
    """ 엔티티에 대한 추상 클래스 """
    ENTITY_COUNT = 0
    
    def __init__(self, x, y, image, strength=0, max_hp=100, attack_range=10, attack_speed=10, move_speed=0):     
        """
        :param x, y: 위치 좌표 (중심점 기준)
        :param image: 미리 로드된 Surface 객체 (ImageLoader에서 받아옴)
        :param strength: 공격력
        :param max_hp: 최대 체력
        :param attack_range: 공격 사거리
        :param attack_speed: 공격 속도
        :param move_speed: 이동 속도
        """        
        super().__init__()
        self.name = 'Entity_' + str(Entity.ENTITY_COUNT)
        ''' 이름 '''
        Entity.ENTITY_COUNT += 1

        # 1. 스탯 설정
        self.strength = strength
        ''' 공격력 '''
        self.max_hp = max_hp
        ''' 최대 체력 '''
        self.attack_range = attack_range
        ''' 공격 사거리 '''
        self.attack_speed = attack_speed
        ''' 공격 속도 '''
        self.move_speed = move_speed
        self.hp = max_hp
        ''' 현재 체력'''
        # 2. 이미지 및 위치 설정
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # 타일의 중심에 배치하기 위해 center 사용
        
        # 3. 이동을 위한 실수 좌표
        self.position = pygame.math.Vector2(x, y)
        self.speed = move_speed

        # 4. 상태 및 타이머
        self.is_dead = False
        self.last_attack_time = 0

    def update(self, dt):
        """ 매 프레임 호출되는 로직 """
        if self.hp <= 0:
            self.die()
            return

        if self.speed != 0:
            self.move(dt)
            
        self.animate(dt)

    def move(self, dt):
        """ 기본 이동 로직 """
        # speed는 pixel/sec 가정, dt는 ms 단위 -> 1000으로 나눔
        self.position.x -= self.speed * (dt / 1000)
        self.rect.centerx = round(self.position.x)

    def die(self):
        self.is_dead = True
        self.kill() # Sprite Group에서 제거

    def setDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def animate(self, dt):
        pass