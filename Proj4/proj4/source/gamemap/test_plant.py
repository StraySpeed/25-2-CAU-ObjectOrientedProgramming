import pygame

class Plant:
    def __init__(self, x, y, image):
        self.image = image                                  # 이미지 불러오기
        self.rect = self.image.get_rect(center=(x, y))      # 불러온 이미지를 기준으로 object 위치 조정
        self.isDead = False                                 # 이 플래그가 True가 되면 타일에서 사라짐

    def draw(self, screen):
        screen.blit(self.image, self.rect)                  # init에서 지정한 위치와 이미지를 가지고 draw
        