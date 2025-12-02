import functools
from ..loader.imageLoader import ImageLoader
from ..gamemap.gamemap import GameMap
from ..gamemap.menubar import Menubar
from ..const import *

# 엔티티를 가져옴
from ..entity import *
#from ..gamemap.test_plant import Plant

class MapSystemManager:
    def __init__(self, screen_width, screen_height, stage_num: int):
        self.width = screen_width
        self.height = screen_height

        # 메뉴바 높이 계산 (전체 높이의 15%)
        self.menu_height = int(self.height * MENU_HEIGHT_RATIO)
        
        # 타일 크기 계산 (가로 꽉 채우기: 너비 / 열 개수)
        # 정사각형 타일을 위해 w, h 동일하게 설정
        # 가로세로 동적으로 써도 되긴한데 지금 tile이 정사각형이라,,
        self.tile_size = self.width // MAP_COLUMNS
        
        # 맵 시작 위치 (메뉴바 바로 아래)
        self.map_start_y = self.menu_height

        # 식물 아이콘 크기 (메뉴바 높이의 80%)
        self.icon_size = int(self.menu_height * 0.8)

        # 1. 스테이지별 타일 이미지 경로 정의

        """self.stage_sprites = {
            1: [
                TILE_DEFAULT_LIST[0],
                TILE_CLICKED_LIST[0],
                TILE_HOVER_LIST[0]
            ],
            2: [
                TILE_DEFAULT_LIST[1],
                TILE_CLICKED_LIST[1],
                TILE_HOVER_LIST[1]
            ],
            3: [
                TILE_DEFAULT_LIST[2],
                TILE_CLICKED_LIST[2],
                TILE_HOVER_LIST[2]
            ]
        }
        paths = self.stage_sprites.get(stage_num)
        self.tile_loader = ImageLoader(*paths)
        """
        self.tile_loader = ImageLoader(TILE_DEFAULT, TILE_CLICKED, TILE_HOVER)
        for i in range(3): self.tile_loader.resize(i, self.tile_size, self.tile_size)

        # 2. 식물/UI 이미지 경로 정의
        self.plant_sprites = PLANT_SPRITE_LIST
        self.plant_loader = ImageLoader(*self.plant_sprites)
        for i in range(len(self.plant_loader.images)): self.plant_loader.resize(i, self.icon_size, self.icon_size)

        # 3. 좀비 스프라이트 로드 & 리사이징
        # 그냥 여기서 로드하고 넘기기
        self.zombie_loader = ImageLoader(*ZOMBIE_SPRITE_LIST)
        # 좀비 크기를 타일 크기와 동일하게 설정
        for i in range(len(self.zombie_loader.images)): self.zombie_loader.resize(i, self.tile_size, self.tile_size)

        # 4. 게임맵, 메뉴바 객체 생성
        self.game_map = GameMap(
            self.tile_loader, 
            x=0, 
            y=self.map_start_y, 
            tileSize=self.tile_size
        )
        
        self.menu_bar = Menubar(
            self.plant_loader, 
            x=0, 
            y=0, 
            w=self.width, 
            h=self.menu_height, 
            icon_size=self.icon_size
        )

    def get_zombie_spawn_pos(self, row_index):
        """
        몇 번째 줄(row)에 좀비를 소환할지 알려주면
        해당 줄의 정확한 (x, y) 픽셀 좌표를 반환하는 메서드

        :param row_index: 좀비를 소환할 행
        :return: 해당 행의 x, y 좌표
        """
        # X 좌표) 화면 오른쪽 끝 + 10
        spawn_x = self.width + 10 
        
        # Y 좌표) 맵 시작 위치 + (줄 번호 * 타일 크기) + (타일 크기 / 2 -> 중앙 정렬)
        spawn_y = self.map_start_y + (row_index * self.tile_size) + (self.tile_size // 2)
        
        return spawn_x, spawn_y

    def get_zombie_image(self, index):
        """
        좀비 스프라이트 반환

        GameManager에서 호출하는 메서드

        :param index: 좀비 인덱스
        """
        return self.zombie_loader.getSprite(index)
    

    def process_events(self, event, plants_group):
        """
        이벤트 처리 및 식물 생성/제거 로직

        :param event: Pygame 이벤트
        :param plants_group: GameManager의 식물 Sprite Group
        """
        # 1. 메뉴바 이벤트 (식물 선택)
        self.menu_bar.eventHandling(event)
        
        # 2. 타일 이벤트 (식물이 선택된 상태일 때만)
        if self.menu_bar.selectedPlantIndex is not None:
            # game_map.eventHandling은 클릭된 Tile 객체를 반환합니다
            clicked_tile = self.game_map.eventHandling(event)
            
            if clicked_tile:
                self._handle_interaction(clicked_tile, plants_group)


    def _handle_interaction(self, tile, plants_group):
        """
        타일 클릭 시 로직 (설치/제거)

        :param tile: 설치할 타일
        :param plants_group: 객체 넣을 그룹(GameManager)
        """
        idx = self.menu_bar.selectedPlantIndex

        # 1. 삽(Index 3)으로 식물 제거
        if idx == 3:
            if tile.isOccupied:
                print("[DEBUG] 식물 제거")
                if tile.plant:
                    tile.plant.kill() # 스프라이트 그룹에서 제거
                tile.plant = None
                # tile.isOccupied = False   # 이거 필요없음
            else:
                print("[DEBUG] 빈 땅입니다.")
        
        # 2. 식물 설치
        else:
            if not tile.isOccupied:
                # 이미지 가져오기
                plant_img = self.plant_loader.getSprite(idx)
                px, py = tile.rect.centerx, tile.rect.centery
                
                # 식물 객체 생성
                new_plant = Peashooter(px, py, plant_img)
                
                # 타일과 스프라이트 그룹 양쪽에 등록
                tile.plant = new_plant
                # tile.isOccupied = True    # 이거 필요없음
                plants_group.add(new_plant)
                
                print(f"[DEBUG] 식물 {idx}번 설치 완료")
            else:
                print("[DEBUG] 이미 식물이 있습니다.")

    def update(self):
        for row in self.game_map.grid:
            for tile in row:
                tile.OnUpdate()

    @staticmethod
    def draw_map_and_menu(func):
        """
        렌더링 순서를 강제하는 데코레이터
        순서: 맵(Background) -> 엔티티(Original Func) -> 메뉴(UI)
        """
        @functools.wraps(func)
        def wrapper(self, screen, *args, **kwargs):
            # 1. [Before] 맵 그리기 (가장 뒤)
            if hasattr(self, 'map_manager'):
                self.map_manager.game_map.draw(screen)
            
            # 2. [Core] 원래의 draw 함수 실행 (중간: 좀비, 식물 등)
            result = func(self, screen, *args, **kwargs)
            
            # 3. [After] 메뉴바 그리기 (가장 앞)
            if hasattr(self, 'map_manager'):
                self.map_manager.menu_bar.draw(screen)
                
            return result
        return wrapper