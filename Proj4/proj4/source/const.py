import os

SOURCE = os.path.join(os.path.dirname(__file__))
RESOURCE = os.path.join(os.path.dirname(os.path.join(os.path.dirname(__file__))), "resource")

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

DEFAULT_COLOR = (200, 200, 200)
HOVER_COLOR = (170, 170, 170)
TEXT_COLOR = BLACK
TITLE_COLOR = (0, 100, 0)


# ===============================
# Level
# ===============================
MAIN_BACKGROUND_IMAGE = TEST_IMAGE
SELECT_LEVEL_BACKGROUND_IMAGE = TEST_IMAGE
LEVEL1_BACKGROUND_IMAGE = TEST_IMAGE
LEVEL2_BACKGROUND_IMAGE = TEST_IMAGE
LEVEL3_BACKGROUND_IMAGE = TEST_IMAGE


ZOMBIE_SPRITE = TEST_SPRITE
LEVEL1 = TEST_LEVEL
LEVEL2 = TEST_LEVEL
LEVEL3 = TEST_LEVEL


# ===============================
# Const
# ===============================
STATE_MENU = "MENU"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_GAME = "GAME"
STATE_PAUSE = "PAUSE"
STATE_GAME_OVER = "GAME_OVER"
STATE_GAME_CLEAR = "GAME_CLEAR"


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