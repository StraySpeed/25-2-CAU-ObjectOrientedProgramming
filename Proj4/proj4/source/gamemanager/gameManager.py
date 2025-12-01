import pygame
from .levelLoader import LevelLoader
from .stateManager import StateManager
from ..entity.basiczombie import BasicZombie 
from ..const import *

class GameManager:
    def __init__(self, screen_width, screen_height, level_file):
        # 1. Sprite 그룹 초기화 (모든 객체를 관리하는 리스트)
        self.plants = pygame.sprite.Group()
        self.zombies: pygame.sprite.Group[BasicZombie] = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.suns = pygame.sprite.Group() # 떨어진 태양들
        
        # 2. 게임 상태 변수
        self.game_over = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state_mgr = StateManager()

        # 3. 타이머 설정 (밀리초 단위)
        self.last_zombie_spawn = pygame.time.get_ticks()
        
        self.last_sun_drop = pygame.time.get_ticks()
        self.sun_drop_rate = 10000     # 10초마다 하늘에서 태양 떨어짐

        # 레벨 데이터 로드
        self.level_loader = LevelLoader(level_file)
        self.sun_balance = self.level_loader.init_sun
        
        # 게임 시작 시간 기준점
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        """
        게임의 매 프레임마다 호출되는 로직
        """
        if self.game_over:
            return

        # 객체 스폰 관리
        self.manage_spawning()

        # 모든 객체 상태 업데이트 (이동, 애니메이션)
        self.plants.update(dt)
        self.zombies.update(dt)
        self.bullets.update(dt)
        self.suns.update(dt)

        # 충돌 처리 (전투 로직의 핵심)
        self.check_collisions()
        
        # 게임 오버 체크 (좀비가 왼쪽 끝에 도달했는지)
        self.check_game_status()

    def draw(self, surface):
        """
        모든 객체를 화면에 그림
        """
        self.plants.draw(surface)
        self.zombies.draw(surface)
        self.bullets.draw(surface)
        self.suns.draw(surface)

        # UI(자원 표시 등)는 추가 필요

    def check_collisions(self):
        """
        충돌 처리 로직
        """
        # 1. 총알이 좀비를 맞췄을 때
        # groupcollide(A, B, dokill_A, dokill_B) -> A는 삭제(True), B는 유지(False)
        hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        for bullet, hit_zombies in hits.items():
            for zombie in hit_zombies:
                zombie.setDamage(20) # 총알 데미지 적용

        # 2. 좀비가 식물을 만났을 때 (먹기 시작)
        # 충돌만 감지하고 제거하지 않음 (False, False)
        collisions = pygame.sprite.groupcollide(self.zombies, self.plants, False, False)
        for zombie, hit_plants in collisions.items():
            if hit_plants:
                # 좀비가 식물을 만나면 멈추고 공격
                target_plant = hit_plants[0] # 가장 먼저 만난 식물
                zombie.speed = 0 # 이동 정지
                zombie.attack(target_plant)
            else:
                # 식물이 사라지면(죽으면) 좀비는 다시 이동
                zombie.speed = 50 

    def manage_spawning(self):
        """
        JSON 데이터에 기반한 스폰
        """
        # 게임 시작 후 경과 시간 계산
        current_time = pygame.time.get_ticks() - self.start_time
        
        # 스폰할 좀비가 있는지 확인
        zombie_data = self.level_loader.get_next_zombie(current_time)
        
        while zombie_data: # 동시에 여러 마리가 나올 수도 있으므로 while
            self.spawn_zombie_from_data(zombie_data)
            # 큐에서 다음 좀비가 또 바로 나와야 하는지 확인
            zombie_data = self.level_loader.get_next_zombie(current_time)

        # 자연 태양 스폰
        if current_time - self.last_sun_drop > self.sun_drop_rate:
            self.last_sun_drop = current_time
            # (미구현) 하늘에서 떨어지는 Sun 객체 생성
            pass

    def spawn_zombie_from_data(self, data):
        """
        JSON 데이터(map_y, name)를 실제 게임 좌표로 변환
        """
        map_y = data['map_y'] # 0 ~ 4 (행 인덱스)
        name = data['name']  
        
        # Grid 좌표(0~4)를 픽셀 좌표로 변환
        # 상단 여백 100px, 한 칸 높이 100px 일 때
        # 사이즈 잘 모르겠음. 조정 필요
        pixel_y = 100 + (map_y * 100) 
        pixel_x = self.screen_width + 20 # 화면 오른쪽 밖
        
        new_zombie = BasicZombie(pixel_x, pixel_y)
        self.zombies.add(new_zombie) # 그룹에 추가
        
        print(f"[DEBUG] Spawned {name} at Row {map_y} (Time: {data['time']})")

    def check_game_status(self):
        """
        좀비가 집(왼쪽 끝)에 도착했는지 확인
        """
#        1. 게임 오버 체크 (좀비가 왼쪽 끝 도달)
        for zombie in self.zombies:
            if zombie.rect.right < 0:
                print("[DEBUG] GAME OVER")
                self.state_mgr.change_state(STATE_GAME_OVER)
                return

        # 2. 게임 클리어 체크
        # 조건: 레벨 로더 큐가 비었고(더 나올 좀비 없음) AND 필드에 좀비가 없음
        if not self.level_loader.zombie_queue and len(self.zombies) == 0:
            print("[DEBUG] GAME CLEAR")
            self.state_mgr.change_state(STATE_GAME_CLEAR)