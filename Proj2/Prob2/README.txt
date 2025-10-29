# Project hierarchy
prob2/
├─ include/              # 헤더 파일(.hpp)
│   ├─ application.h
│   ├─ calculator.h
│   ├─ inf_int.h
│   └─ precedence.h
│
├─ src/                  # 소스 파일(.cpp)
│   ├─ application.cpp
│   ├─ calculator.cpp
│   ├─ devide.cpp
│   ├─ inf_int.cpp
│   ├─ precedence.cpp
│   ├─ sqrt.cpp
│
├─ pysrc/                # Python 소스 파일(.pyd)
│   ├─ calculator.pyd
│
├─ wrapper.py	# C++ to Python wrapper
├─ setup.py	# C++ to Python
├─ main.cpp	# main() 포함
├─ main.py	# Python GUI
├─ file1.txt
├─ Makefile
├─ requirements.txt
├─ README.txt


# Basic Info
## 1. C++
Compiled with GCC 12.2.0, 64 bit
C++17, windows 11

## 2. Python
Python 3.10.0

```
requirements.txt
tk
pybind11
```

------
# C++
# Compile & Run Command
>>> make
>>> .\prob2.exe

------
# Python
# Run Command
>>> python main.py