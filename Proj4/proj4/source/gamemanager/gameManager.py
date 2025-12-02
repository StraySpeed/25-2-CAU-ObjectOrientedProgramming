import pygame
from ..loader.levelLoader import LevelLoader
from ..loader.imageLoader import ImageLoader
from .stateManager import StateManager
from .mapSystemManager import MapSystemManager
from ..entity.basiczombie import BasicZombie 
from ..const import *

class GameManager:
    def __init__(self, screen_width, screen_height, level):
        # 1. Sprite 그룹 초기화 (모든 객체를 관리하는 리스트)
        self.plants = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.suns = pygame.sprite.Group() # 떨어진 태양들
        
        # 2. 게임 상태 변수
        self.game_over = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state_mgr = StateManager()
        self.map_manager = MapSystemManager(screen_width, screen_height, level)

        # 3. 타이머 설정 (밀리초 단위)
        self.last_zombie_spawn = pygame.time.get_ticks()
        
        self.last_sun_drop = pygame.time.get_ticks()
        self.sun_drop_rate = 10000     # 10초마다 하늘에서 태양 떨어짐

        # 레벨 데이터 로드
        level_file = get_game_level(level)
        self.level_loader = LevelLoader(level_file)
        self.sun_balance = self.level_loader.init_sun
        
        # 게임 시작 시간 기준점
        self.start_time = pygame.time.get_ticks()

    def handle_input(self, event):
        """
        사용자 입력 처리
        """
        # 맵/메뉴 관련 처리를 매니저에게 위임
        # 식물이 생성되면 self.plants 그룹에 넣어야 하므로 그룹을 인자로 넘김
        self.map_manager.process_events(event, self.plants)

    def update(self, dt):
        """
        게임의 매 프레임마다 호출되는 로직
        """
        if self.game_over:
            return

        # 맵 타일 업데이트
        self.map_manager.update()

        # 객체 스폰 관리
        self.manage_spawning()

        # 모든 객체 상태 업데이트 (이동, 애니메이션)
        self.plants.update(dt)
        self.zombies.update(dt)
        self.bullets.update(dt)
        self.suns.update(dt)

        # 충돌 처리
        self.check_collisions()
        
        # 게임 오버 체크 (좀비가 왼쪽 끝에 도달했는지)
        self.check_game_status()

    @MapSystemManager.draw_map_and_menu
    def draw(self, surface):
        """
        모든 객체를 화면에 그림
        """
        self.plants.draw(surface)
        self.zombies.draw(surface)
        self.bullets.draw(surface)
        self.suns.draw(surface)

    def check_collisions(self):
        """
        충돌 처리 로직
        """
        # 1. 총알 vs 좀비
        hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        for bullet, hit_zombies in hits.items():
            for zombie in hit_zombies:
                zombie.setDamage(20)

        # 2. 좀비 vs 식물
        for zombie in self.zombies:
            # 해당 좀비와 충돌한 식물들을 찾음
            hit_plants = pygame.sprite.spritecollide(zombie, self.plants, False)
            
            if hit_plants:
                # 식물을 만남 -> 멈추고 공격
                zombie.speed = 0  # 이동 정지
                
                # 가장 앞에 있는(먼저 충돌한) 식물 하나만 공격
                target_plant = hit_plants[0]
                
                # 공격 시도 (쿨타임은 zombie.attack 내부에서 체크)
                zombie.attack(target_plant)
                
            else:
                # 앞에 식물이 없음 (죽어서 사라졌거나 원래 없었음) -> 다시 이동
                # 원래 속도로 복구
                zombie.speed = zombie.move_speed

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
        
        spawn_x, spawn_y = self.map_manager.get_zombie_spawn_pos(map_y)
        
        new_zombie = BasicZombie(spawn_x, spawn_y, self.map_manager.get_zombie_image(0))
        self.zombies.add(new_zombie) # 그룹에 추가
        
        print(f"[DEBUG] Spawned {name} at Row {map_y} (Time: {data['time']})")


    def check_game_status(self):
        """
        좀비가 집(왼쪽 끝)에 도착했는지 확인
        """
        # 1. 게임 오버 체크 (좀비가 왼쪽 끝 도달)
        for zombie in self.zombies:
            if zombie.rect.right < 0:
                print("[DEBUG] GAME OVER")
                self.state_mgr.change_state(STATE_GAME_OVER)
                return

        # 2. 게임 클리어 체크
        # 조건) 레벨 로더 큐가 비었고(더 나올 좀비 없음) AND 필드에 좀비가 없음
        if not self.level_loader.zombie_queue and len(self.zombies) == 0:
            print("[DEBUG] GAME CLEAR")
            self.state_mgr.change_state(STATE_GAME_CLEAR)