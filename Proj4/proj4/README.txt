# Project hierarchy
proj4/
├─ resource/              # 리소스 파일(스프라이트, 음악 등)
│   ├─ bullet/
│   ├─ card/
│   ├─ character/
│   └─ font/
│   └─ interface/
│   └─ map/
│
├─ source/                  # 소스 파일(.py)
│   ├─ entity/              # 엔티티에 대한 정의(식물, 좀비 등)
│   │  ├─ bullet.py
│   │  ├─ entity.py         # base class
│   │  ├─ plant.py
│   │  ├─ sun.py
│   │  ├─ zombie.py
│   │
│   ├─ gamemanager/         # 게임 시스템 매니저
│   │  ├─ gameManager.py
│   │  ├─ mapSystemManager.py
│   │  ├─ stateManager.py
│   │  ├─ uiManager.py
│   │
│   ├─ gamemap/             # 게임 맵, 메뉴바
│   │  ├─ gamemap.py
│   │  ├─ menubar.py
│   │  ├─ tile.py
│   │
│   ├─ levels/             # 스테이지 정의
│   │  ├─ level_1.json
│   │  ├─ level_2.json
│   │  ├─ level_3.json
│   │
│   ├─ loader/             # 기본 설정 로드하는 헬퍼들
│   │  ├─ fontLoader.py
│   │  ├─ imageLoader.py
│   │  ├─ levelLoader.py
│   │
│   ├─ app.py               # Entry point
│   ├─ const.py             # CONSTANT
│   ├─ settings.json        # 기본 게임 설정
│
├─ .gitignore
├─ main.py
├─ README.txt
├─ requirements.txt


# Basic Info
Windows 11, 64 bit

## Python
Python 3.10.0

```
requirements.txt
pygame==2.6.1
```

------
# Python
# Run Command
>>> python main.py