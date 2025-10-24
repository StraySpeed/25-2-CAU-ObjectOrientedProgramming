# 컴파일러 & 옵션
CXX = g++
CXXFLAGS = -Wall -std=c++17 -I./$(INC_DIR)

# src 경로, include 경로, obj 경로
SRC_DIR = src
INC_DIR = include
OBJ_DIR = obj

# src 디렉토리의 모든 .cpp 파일을 지정
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
# obj 디렉토리의 모든 .o 파일을 지정
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))
# 출력 파일명
TARGET = prob2

# OS 기반, MKDIR과 RM 정의
ifeq ($(OS),Windows_NT)
       MKDIR = if not exist $(1) mkdir $(1)
       RM = rmdir /S /Q $(1) 2>nul || del /Q $(1) 2>nul
else
       MKDIR = mkdir -p $(1)
       RM = rm -rf $(1)
endif

# 규칙
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(SRCS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR):
	$(call MKDIR,$(OBJ_DIR))
       
clean:
	$(call RM,$(OBJ_DIR))
	$(call RM,$(TARGET))