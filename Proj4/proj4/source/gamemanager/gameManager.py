import pygame
from ..loader.levelLoader import LevelLoader
from ..loader.imageLoader import ImageLoader
from .stateManager import StateManager
from .mapSystemManager import MapSystemManager
from ..entity.zombie import BasicZombie 
from ..const import *
from ..entity.bullet import Bullet
from ..entity.sun import Sun

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
        self.sun_drop_rate = 5000

        # 레벨 데이터 로드
        level_file = get_game_level(level)
        self.level_loader = LevelLoader(level_file)
        self.sun_balance = self.level_loader.init_sun
        
        # 게임 시작 시간 기준점
        self.start_time = pygame.time.get_ticks()

        self.sun_loader = ImageLoader(SUN_SPRITE)
        self.sun_loader.resize(0, screen_width / MAP_ROWS * 0.5, screen_height / MAP_COLUMNS * 0.5)
        self.sun_image = self.sun_loader.getSprite(0)

    def handle_input(self, event):
        """
        사용자 입력 처리
        """
        # 태양에 대한 처리는 여기서 수행
        # 맵/메뉴 처리는 mapSystem에서 수행
        # 1. 태양 클릭 수집
        # 겹쳐있는 태양 중 하나만 클릭되도록 break 사용
        clicked_sun = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sun in self.suns:
                value = sun.handle_event(event)
                if value > 0:
                    self.sun_balance += value
                    sun.kill() # 수집된 태양 제거
                    print(f"[DEBUG] Sun collected! Balance: {self.sun_balance}")
                    clicked_sun = True
                    break # 한 번에 하나만 수집
        
        # 태양을 클릭하지 않았을 때만 맵 상호작용
        if not clicked_sun:
            # 2. 맵/메뉴 처리 (현재 잔고를 넘겨주고, 사용한 비용을 받아옴)
            spent_sun = self.map_manager.process_events(event, self.plants, self.sun_balance)
            
            if spent_sun > 0:
                self.sun_balance -= spent_sun
                print(f"[DEBUG] Plant placed. Cost: {spent_sun}, Remaining: {self.sun_balance}")
                # 설치 후 선택 해제 (PvZ 스타일)
                self.map_manager.menu_bar.selectedPlantIndex = None


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
        # 식물 업데이트 처리
        for plant in self.plants:
            # Peashooter는 attack, Sunflower는 obtain_sun
            if hasattr(plant, 'obtain_sun'): 
                new_sun = plant.obtain_sun()
                if new_sun:
                    self.suns.add(new_sun)
            
            # Peashooter 공격
            if hasattr(plant, 'attack'):
                bullet = plant.attack(self.zombies)
                if isinstance(bullet, Bullet): self.bullets.add(bullet)

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

    def draw_sun_balance(self, surface):
        # 현재 자원(UI) 표시
        font = pygame.font.Font(None, 36)
        text = font.render(f"Sun: {self.sun_balance}", True, BLACK)
        surface.blit(text, (self.screen_width - font.get_linesize() - 100, font.get_height() + 25)) # 메뉴바 근처에 표시

    def check_collisions(self):
        """
        충돌 처리 로직
        """
        # 1. 총알 vs 좀비
        hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        for bullet, hit_zombies in hits.items():
            for zombie in hit_zombies:
                zombie.setDamage(bullet.strength)
                bullet.kill()

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
            self.sun_balance += SUN_VALUE
            print(f"[DEBUG] {SUN_VALUE} of Sun Dropped")
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