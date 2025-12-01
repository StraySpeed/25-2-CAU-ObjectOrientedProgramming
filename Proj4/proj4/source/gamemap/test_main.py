import sys
import pygame
import imageLoader
import gamemap
import menubar
import test_plant as plant

pygame.init()
# 맘대로 지정한 창 크기
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("map")
clock = pygame.time.Clock()

# Initializing
# ImageLoader class에서 이미지 한번에 관리하기
# imageLoader.py 확인
# GameMap, Menubar에 이미지를 넣으면 해당 이미지로 맵과 UI 생성,
# 인자에 크기도 넣을 수 있음. gamemap.py, menubar.py 확인
############################## Initialize Part ##################################
#################################################################################
# 게임 스테이지 선택
currentStage = 1

# Image Loading: Tile Sprites
stageSprites = {
    1: [ # 스테이지 1
        "../../asset/sprite/tile_default_1.png",
        "../../asset/sprite/tile_clicked_1.png",
        "../../asset/sprite/tile_hover_1.png"
    ],
    2: [ # 스테이지 2
        "../../asset/sprite/tile_default_2.png",
        "../../asset/sprite/tile_clicked_2.png",
        "../../asset/sprite/tile_hover_2.png"
    ],
    3: [ # 스테이지 3
        "../../asset/sprite/tile_default_3.png",
        "../../asset/sprite/tile_clicked_3.png",
        "../../asset/sprite/tile_hover_3.png"
    ]
}
tileImageLoader = imageLoader.ImageLoader(*stageSprites[currentStage])
for i in range(3): tileImageLoader.resize(i, 120, 120)

# Image Loading: Menubar UI Sprites
plantImageLoader = imageLoader.ImageLoader(
    "../../asset/sprite/plant_shooter.png",    # 인덱스 0
    "../../asset/sprite/plant_sunflower.png",  # 인덱스 1
    "../../asset/sprite/plant_defender.png",   # 인덱스 2
    "../../asset/sprite/shovel.png"            # 인덱스 3
)
for i in range(4): plantImageLoader.resize(i, 100, 100)

# 맵, Menubar UI 생성
gameMap = gamemap.GameMap(tileImageLoader)
menuBar = menubar.Menubar(plantImageLoader)

############################## Initialize Part 종료 ##############################
#################################################################################


# Menubar에서 어떤 식물을 심을 건지(혹은 식물을 없앨 건지) 선택을 한 후에 Tiles(gamemap)과 상호작용 가능
################################# Update Part ##################################
################################################################################
running = True
while running:
    ### event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # menubar 이벤트 확인, menubar에서 식물 생성 버튼이 눌렸는지
        menuBar.eventHandling(event)
        # 설치할 식물을 선택했을 때만 tile들과 상호작용 가능
        if menuBar.selectedPlantIndex is not None:
            clickedTile = gameMap.eventHandling(event)
        
            # 뭔가 클릭된 타일이 있다면
            if clickedTile:
                # menubar에서 선택했던 버튼이 식물 제거 버튼이면
                if menuBar.selectedPlantIndex == 3:
                    if clickedTile.isOccupied:
                        print("식물 제거")
                        clickedTile.plant = None
                    else:
                        print("빈 땅")
                # menubar에서 선택했던 버튼이 어떤 식물이면
                else:
                    # 클릭한 tile에 식물이 없을 때만
                    if not clickedTile.isOccupied:
                        # menubar에서 선택한 식물의 이미지 가져오기
                        plantIdx = menuBar.selectedPlantIndex
                        plantImage = plantImageLoader.getSprite(plantIdx)

                        # 클릭한 tile의 위치에 식물 심기
                        px = clickedTile.rect.centerx
                        py = clickedTile.rect.centery
                        newPlant = plant.Plant(px, py, plantImage)
                        clickedTile.plant = newPlant
                        print(f"식물 {menuBar.selectedPlantIndex}번 설치됌")
                    else:
                        print("해당 Tile에 식물 이미 존재")
        else:
            # menubar에서 아무 버튼도 선택 안 되어 있으면, tile의 모든 상호작용(hover, click) 안 함
            pass

    ### update
    # map의 모든 tiles 업데이트
    # tile의 isOccupied 초기화용, 식물이 죽었으면 False로 바꾸기 위해
    for row in gameMap.grid:
        for tile in row:
            tile.OnUpdate()
    

    ### draw
    screen.fill((50, 50, 50))
    
    # gamemap, menubar darw
    gameMap.draw(screen)
    menuBar.draw(screen)

    pygame.display.flip()
    clock.tick(60)
################################ Update Part 종료 ################################
#################################################################################

pygame.quit()
sys.exit()