import pygame
import abc

class Entity(pygame.sprite.Sprite, abc.ABC):
    """ 엔티티에 대한 추상 클래스 """
    ENTITY_COUNT = 0
    def __init__(self, x, y, image_path, strength = 0, max_hp = 100, attack_range = 10, attack_speed = 10, move_speed = 0):     
        """
        initializer
        ------
        :param x, y: x, y 위치
        :param image_path: 스프라이트 경로(추후 지정 예정)
        :param strength: 공격력
        :param max_hp: 최대 체력
        :param attack_range: 공격 사거리
        :param attack_speed: 공격 속도
        :param move_speed: 이동 속도
        """        
        super().__init__();   
        self.name = 'Entity_' + str(Entity.ENTITY_COUNT)
        ''' 이름 '''
        self.strength = strength
        ''' 공격력 '''
        self.max_hp = max_hp
        ''' 최대 체력 '''
        self.attack_range = attack_range
        ''' 공격 사거리 '''
        self.attack_speed = attack_speed
        ''' 공격 속도 '''
        self.move_speed = move_speed
        ''' 이동 속도 '''
        Entity.ENTITY_COUNT += 1

        # 1. 이미지 및 위치 설정
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except:
            # 이미지가 없을 경우 디버깅용 빨간 사각형 생성
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # 2. 이동을 위한 실수 좌표
        self.position = pygame.math.Vector2(x, y)
        self.speed = move_speed

        # 3. 게임 플레이 속성
        self.hp = self.max_hp
        self.is_dead = False
        
        # 4. 상태 및 타이머 (공격 쿨타임 등)
        self.last_attack_time = 0

    def update(self, dt):
        """
        Gameloop 내에서 매 프레임 호출되는 메인 로직

        :param dt: 델타 타임 (프레임 간 시간 차이)
        """
        if self.hp <= 0:
            self.die()
            return

        if self.speed != 0:
            self.move(dt)
            
        # 자식 클래스별 고유 행동 수행 (애니메이션, 특수 능력 등)
        self.animate(dt)

    def move(self, dt):
        """
        기본 이동 로직 (왼쪽/오른쪽)
        좀비가 주로 사용
        """
        self.position.x -= self.speed * dt
        self.rect.x = round(self.position.x)

    def die(self):
        """
        엔티티 사망 시 제거
        """
        self.is_dead = True
        self.kill()

    def setDamage(self, damage):
        """
        데미지 받는 로직
        """
        self.health -= damage
        if self.hp <= 0:
            self.die()

    @abc.abstractmethod
    def attack(self):
        """
        엔티티가 공격하는 로직
        """
        pass

    @abc.abstractmethod
    def animate(self):
        """
        엔티티의 행동 로직
        """
        pass