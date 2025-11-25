import pygame
import sys

class Menubar:
    def __init__(self):
        pass

class Button:
    def __init__(self, x, y, w, h, sprite, clickSprite):
        # x, y, width, height
        self.rect = pygame.Rect(x, y, w, h)
        
        # sprites
        self.defaultSprite = sprite
        self.clickSprite = clickSprite
        
        # pressed 상태 여부
        self.isPressed = False
        # event 실행 여부
        self.eventTrigger = False

    
    def Draw(self, screen):
        sprite = self.defaultSprite
        
        if (self.isPressed):
            sprite = self.clickSprite
        
        screen.blit(sprite, self.rect)

    def IsClicked(self, event):
        self.eventTrigger = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.isPressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.isPressed = False
                if self.rect.collidepoint(event.pos):
                    self.eventTrigger = True
        
        return self.eventTrigger
    

######################### 테스트용 #########################
###########################################################
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()


rawDefaultSprite = pygame.image.load("../../asset/sprite/ender_eye.png")
rawClickSprite = pygame.image.load("../../asset/sprite/ender_pearl.png")
defaultSprite = pygame.transform.scale_by(rawDefaultSprite, 5)
clickSprite = pygame.transform.scale_by(rawClickSprite, 5)

button = Button(300, 300, 80, 80, defaultSprite, clickSprite)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if button.IsClicked(event):
            print("Clicked")

    screen.fill((0, 0, 0))
    
    button.Draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()