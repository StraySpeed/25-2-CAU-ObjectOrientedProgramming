import pygame
import tile

class Menubar:
    def __init__(self, imageLoader, x = 10, y = 10, w = 400, h = 100):
        self.rect = pygame.Rect(x, y, w, h)     # 메뉴 바, 1280*720 기준 (10, 10)에서 시작, 400*100
        self.plantSummonButtons = []            # 식물 설치 버튼
        self.selectedPlantIndex = None          # 식물 번호 0, 1, 2 (shooter, sunflower, defender)

        # 버튼 시작 위치 조정, 1280*720 기준 10, 10
        startX = x
        startY = y
        
        # 식물 버튼 3개 생성
        for i in range(4):
            # 버튼 위치 잡기
            buttonX = startX + (i * 100)
            buttonY = startY
            buttonRect = pygame.Rect(buttonX, buttonY, 100, 100)
            
            # 식물 이미지 가져오기
            plantImage = imageLoader.getSprite(i) 
            self.plantSummonButtons.append({'rect': buttonRect, 'image': plantImage, 'id': i})
    
    def draw(self, screen):
        # 메뉴 바 그리기
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        
        # 버튼 그리기
        for button in self.plantSummonButtons:
            # 선택된 버튼은 테두리를 빨간색으로 강조
            color = (255, 0, 0) if self.selectedPlantIndex == button['id'] else (0, 0, 0)  
            pygame.draw.rect(screen, (150, 150, 150), button['rect'])                      # 버튼 배경
            screen.blit(button['image'], button['rect'])                                   # 식물 아이콘
            pygame.draw.rect(screen, color, button['rect'], 3)                             # 테두리

    # 특정 식물 버튼을 누르면, 계속 tile을 누를 수 있는 상태로 유지
    # 
    def eventHandling(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.plantSummonButtons:
                    if button['rect'].collidepoint(event.pos):
                        # 이미 선택된 걸 또 누르면 취소, 아니면 선택
                        if self.selectedPlantIndex == button['id']:
                            self.selectedPlantIndex = None
                        else:
                            self.selectedPlantIndex = button['id']
                        return True # UI가 클릭되었다는 신호
        return False