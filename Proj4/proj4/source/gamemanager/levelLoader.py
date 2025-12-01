import json
from collections import deque

class LevelLoader:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)
            
        # 1. 초기 자원 설정 가져오기
        self.init_sun = self.data.get('init_sun_value', 50)
        
        # 2. 좀비 리스트를 시간 순서대로 정렬
        raw_zombie_list = self.data.get('zombie_list', [])
        sorted_list = sorted(raw_zombie_list, key=lambda z: z['time'])
        
        # 3. 큐(Queue)로 변환하여 저장
        self.zombie_queue = deque(sorted_list)
        
    def get_next_zombie(self, current_time):
        """
        현재 시간에서 소환되는 좀비 반환

        JSON 형식

        {"time":20000, "map_y":0, "name":"Zombie"} 의 형태가 반환

        :param current_time: 타임 (현재 시간)
        :return: Zombie JSON format data (없으면 None)
        """
        if not self.zombie_queue:
            return None # 더 이상 나올 좀비가 없음
            
        # 큐의 맨 앞(가장 빠른 시간) 좀비 확인
        next_zombie = self.zombie_queue[0]
        
        if current_time >= next_zombie['time']:
            return self.zombie_queue.popleft() # 큐에서 제거하고 반환
        return None