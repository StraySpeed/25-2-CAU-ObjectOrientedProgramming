import tile

class GameMap:
    def __init__(self, imageLoader, x = 0, y = 120, rows = 5, columns = 10, tileSize = 120):
        self.grid = []              # 맵 배열
        self.rows = rows            # 세로 칸 개수
        self.columns = columns      # 가로 칸 개수
        self.tileSize = tileSize    # size, 1280*720 기준 120*120
        
        # 타일 시작 위치 조정, 1280*720 기준 0, 120
        startX = x
        startY = y
        
        # tile 생성
        for row in range(rows):
            rowList = []
            for column in range(columns):
                # 타일 위치 조정
                x = startX + (column * tileSize)
                y = startY + (row * tileSize)
                
                # row 한 줄에 tile 10개 넣고
                new_tile = tile.Tile(x, y, tileSize, tileSize, imageLoader)
                rowList.append(new_tile)
            # grid에 row 5개 넣기
            self.grid.append(rowList)

    def draw(self, screen):
        # tile들 하나하나 draw
        for row_list in self.grid:
            for tile in row_list:
                tile.draw(screen)

    def eventHandling(self, event):
        # tile들 하나하나에서 event 확인
        for row_list in self.grid:
            for tile in row_list:
                if tile.eventHandling(event):
                    return tile
        
        return None
    