import os

SOURCE = os.path.join(os.path.dirname(__file__))
RESOURCE = os.path.join(os.path.dirname(os.path.join(os.path.dirname(__file__))), "resource")
ASSET = os.path.join(os.path.dirname(os.path.join(os.path.dirname(__file__))), "asset")

GAME_FONT = os.path.join(RESOURCE, "font", "EFjejudoldam.ttf")
""" 게임 폰트 """
SETTINGS = os.path.join(SOURCE, "settings.json")
""" settings.json """



# ===============================
# 테스트용 파일 경로
# ===============================
TEST_IMAGE = os.path.join(RESOURCE, "test_background.jpg")
""" TEST_IMAGE """
TEST_SPRITE = os.path.join(RESOURCE, "test_sprite.png")
""" TEST_SPRITE """
TEST_LEVEL = os.path.join(SOURCE, "levels", "test_level.json")
""" TEST_LEVEL """


# ===============================
# Color
# ===============================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

DEFAULT_COLOR = (200, 200, 200)
HOVER_COLOR = (170, 170, 170)
TEXT_COLOR = BLACK
TITLE_COLOR = (0, 100, 0)
MENUBAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)

# ===============================
# Level
# ===============================
MAIN_BACKGROUND_IMAGE = os.path.join(RESOURCE, "interface", "mainmenu.png")
SELECT_LEVEL_BACKGROUND_IMAGE = os.path.join(RESOURCE, "interface", "selectmenu.png")
LEVEL1_BACKGROUND_IMAGE = TEST_IMAGE
LEVEL2_BACKGROUND_IMAGE = TEST_IMAGE
LEVEL3_BACKGROUND_IMAGE = TEST_IMAGE

VICTORY_OVERLAY = os.path.join(RESOURCE, "interface", "victory.png")
DEFEAT_OVERLAY = os.path.join(RESOURCE, "interface", "defeat.png")

BUTTON_LIST = []

MAP_COLUMNS = 9   # 가로 타일 개수
MAP_ROWS = 5      # 세로 타일 개수
MENU_HEIGHT_RATIO = 0.15 # 화면 높이 대비 메뉴바 비율 (15%)

ZOMBIE_SPRITE = TEST_SPRITE
LEVEL1 = os.path.join(SOURCE, "levels", "level_1.json")
LEVEL2 = os.path.join(SOURCE, "levels", "level_2.json")
LEVEL3 = os.path.join(SOURCE, "levels", "level_3.json")


# ===============================
# Const
# ===============================
STATE_MENU = "MENU"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_GAME = "GAME"
STATE_PAUSE = "PAUSE"
STATE_GAME_OVER = "GAME_OVER"
STATE_GAME_CLEAR = "GAME_CLEAR"

# ===============================
# TILE SPRITE
# ===============================
TILE_DEFAULT = os.path.join(RESOURCE, "map", "map_default.png")
TILE_CLICKED = os.path.join(RESOURCE, "map", "map_hover.png")
TILE_HOVER = os.path.join(RESOURCE, "map", "map_hover.png")

# 아래는 테스트 에셋
TILE_DEFAULT_1 = os.path.join(ASSET, "sprite", "tile_default_1.png")
TILE_DEFAULT_2 = os.path.join(ASSET, "sprite", "tile_default_2.png")
TILE_DEFAULT_3 = os.path.join(ASSET, "sprite", "tile_default_3.png")
TILE_DEFAULT_LIST = [
    TILE_DEFAULT_1,
    TILE_DEFAULT_2,
    TILE_DEFAULT_3
    ]

TILE_CLICKED_1 = os.path.join(ASSET, "sprite", "tile_clicked_1.png")
TILE_CLICKED_2 = os.path.join(ASSET, "sprite", "tile_clicked_2.png")
TILE_CLICKED_3 = os.path.join(ASSET, "sprite", "tile_clicked_3.png")
TILE_CLICKED_LIST = [
    TILE_CLICKED_1,
    TILE_CLICKED_2,
    TILE_CLICKED_3
    ]

TILE_HOVER_1 = os.path.join(ASSET, "sprite", "tile_hover_1.png")
TILE_HOVER_2 = os.path.join(ASSET, "sprite", "tile_hover_2.png")
TILE_HOVER_3 = os.path.join(ASSET, "sprite", "tile_hover_3.png")
TILE_HOVER_LIST = [
    TILE_HOVER_1,
    TILE_HOVER_2,
    TILE_HOVER_3
    ]

# ===============================
# PLANT SPRITE
# ===============================
#PLANT_SHOOTER = os.path.join(ASSET, "sprite", "plant_shooter.png")
#PLANT_SUNFLOWER = os.path.join(ASSET, "sprite", "plant_sunflower.png")
#PLANT_DEFENDER = os.path.join(ASSET, "sprite", "plant_defender.png")
PLANT_SHOOTER = os.path.join(RESOURCE, "character", "attack_plant.png")
PLANT_SUNFLOWER = os.path.join(RESOURCE, "character", "sunflower.png")
PLANT_DEFENDER = os.path.join(RESOURCE, "character", "walnut.png")

SHOVEL = os.path.join(ASSET, "sprite", "shovel.png")

PLANT_SPRITE_LIST = [
    PLANT_SHOOTER,
    PLANT_SUNFLOWER,
    PLANT_DEFENDER,
    SHOVEL
]

BULLET_SPRITE = os.path.join(RESOURCE, "bullet", "bullet.png")
BULLET_BROKEN_SPRITE = os.path.join(RESOURCE, "bullet", "broken_bullet.png")

# ===============================
# ZOMBIE SPRITE
# ===============================
ZOMBIE_BASIC = os.path.join(RESOURCE, "character", "zombie1.png")
ZOMBIE_POWER = os.path.join(RESOURCE, "character", "zombie2.png")
ZOMBIE_SPRITE_LIST = [  
    ZOMBIE_BASIC,
    ZOMBIE_POWER
]

# ===============================
# SUN COST
# ===============================
SUN_SPRITE = os.path.join(RESOURCE, "character", "sun.png")
SUN_VALUE = 25
PLANT_COSTS = {
    0: 100, # Peashooter
    1: 50,  # Sunflower
    2: 50,  # Wallnut
    3: 0    # Shovel
}

def get_game_level(level):
    """
    해당하는 레벨 json 파일 반환

    :param level: (int) 레벨
    :return: json file path (없으면 TEST_LEVEL)
    """
    if level == 1:
        return LEVEL1
    if level == 2:
        return LEVEL2
    if level == 3:
        return LEVEL3
    
    print("[ERROR] Cannot Find Level. Load TEST_LEVEL.")
    return TEST_LEVEL