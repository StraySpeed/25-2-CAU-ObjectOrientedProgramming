import pygame

class ImageLoader:
    def __init__(self, *spriteFilePath):
        # 원본 파일 위치
        self.spriteFilePath = spriteFilePath
        # load된 sprites
        self.images = []

        # loading
        # 실패 시 그냥 투명한 공간으로
        for sprite in self.spriteFilePath:
            try:
                self.images.append(pygame.image.load(sprite).convert_alpha())
            except (FileNotFoundError):
                print(f"Failed to load image: {sprite}")
                self.images.append(pygame.Surface((120, 120), pygame.SRCALPHA))
    
    # image를 특정 크기로 강제 조정
    def resize(self, n, width, height):
        if (n >= len(self.images) or n < 0):
            print(f"Unvalid index: {n}")
            return False
        
        self.images[n] = pygame.transform.scale(self.images[n], (width, height))
    
    # 특정 image 가져오기
    def getSprite(self, n):
        if (n >= len(self.images) or n < 0):
            print(f"Unvalid index: {n}")
            return False
        
        return self.images[n]