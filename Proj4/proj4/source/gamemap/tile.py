import pygame

class Tile:
    def __init__(self, x, y, w, h, sprite):
        # x, y, width, height
        self.rect = pygame.Rect(x, y, w, h)
        
        # sprites
        # 
        self.defaultSprite = sprite.getSprite(0)
        self.clickSprite = sprite.getSprite(1)
        self.hoverSprite = sprite.getSprite(2)
        
        # pressed 상태 여부
        self.isPressed = False
        # hovering 상태 여부
        self.isHovering = False
        # event 실행 여부
        self.eventTrigger = False
        
        # tile에 있는 식물
        self.plant = None
    
    # tile에 plant가 있는지 = plant에 뭐가 들어있는지
    @property
    def isOccupied(self):
        return self.plant is not None

    # plant가 죽으면 tile 비우기 = plant 비우기
    # main의 update에서 실행
    def OnUpdate(self):
        if self.plant and self.plant.isDead:
            print("식물 제거")
            self.plant = None
    
    def draw(self, screen):
        # sprite 결정
        # default의 경우
        sprite = self.defaultSprite
        # hovering의 경우
        if (self.isHovering):
            sprite = self.hoverSprite
        # pressed의 경우
        if (self.isPressed):
            sprite = self.clickSprite
        
        # 그리기
        screen.blit(sprite, self.rect)

        # 식물이 있으면 그리기
        if self.plant:
            self.plant.draw(screen)


    def eventHandling(self, event):
        self.eventTrigger = False
        
        # 마우스 움직임 (hovering) 감지
        if event.type == pygame.MOUSEMOTION:
            self.isHovering = self.rect.collidepoint(event.pos)

        # 마우스 클릭 감지
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.isPressed = True
        # 클릭 후에, 마우스를 tile 위에서 땠을 때만 이벤트 발생
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.isPressed and self.rect.collidepoint(event.pos):
                    self.eventTrigger = True
                self.isPressed = False

        return self.eventTrigger
    