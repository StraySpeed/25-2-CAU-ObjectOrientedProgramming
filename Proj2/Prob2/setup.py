import sys
from setuptools import setup, Extension
import pybind11

# 컴파일러에 따른 추가 옵션 설정
# C++17 표준을 사용하고, 최적화 레벨을 3으로 설정합니다.
extra_compile_args = ['-std=c++17', '-O3']
if sys.platform == 'win32':
    extra_compile_args = ['/std:c++17', '/O2']

# 래핑할 C++ 모듈에 대한 정보를 담는 Extension 객체 생성
ext_modules = [
    Extension(
        # 1. 최종적으로 생성될 파이썬 모듈 이름 (import precedence_wrapper)
        'pysrc.precedence_wrapper',
        
        # 2. 컴파일할 소스 파일 목록
        #    - 바인딩 코드(wrapper.cpp)와 필요한 모든 C++ 소스 파일을 포함해야 합니다.
        #    - main.cpp는 파이썬 모듈에 포함되면 안 됩니다.
        sources=[
            'src/wrapper.cpp',
            'src/precedence.cpp',
        ],
        
        # 3. 헤더 파일이 있는 디렉토리
        include_dirs=[
            'include',
            pybind11.get_include()
        ],
        
        # 4. 언어 설정
        language='c++',
        
        # 5. 추가 컴파일 옵션
        extra_compile_args=extra_compile_args
    ),
]

# setup() 함수 호출
setup(
    name='precedence_wrapper',
    version='0.1.0',
    packages=['pysrc'],
    ext_modules=ext_modules,
)