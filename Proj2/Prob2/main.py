from pysrc import calculator
from tkinter import Tk, ttk
from tkinter import *

class Application(Tk):
    WIDTH = '500'
    HEIGHT = '600'
    OPERATORS = ['+', '-', '/', '*', '%', '^', 'SQRT', '(', ')']
    ROW = 8
    COLUMN = 4
    def __init__(self):
        super().__init__()
        self.title("Inf_int Calculator")
        self.geometry(str(Application.WIDTH) + 'x' +  str(Application.HEIGHT) + '+0+0')
        self.resizable(True, True)
        self.calculator = calculator.Calculator()

        # 수식 입력, 출력 창
        self.display_main = None
        self.display_result = None
        # 버튼 프레임
        self.buttonFrame = None

        # 1. 계산기 양식처럼 칸을 나눔
        self.divideByWeight()

        # 2. 수식 입출력 창 생성
        self.createDisplay()

        # 3. 입력 버튼 생성
        self.createButton()

    def divideByWeight(self):
        # 창의 행과 열이 동적으로 크기 조절되도록 설정
        # 8 row x 4 column
        # column 가중치는 전부 동일하게
        for i in range(Application.COLUMN):
            self.grid_columnconfigure(i, weight=1)

        # row 가중치는 계산화면2 정답화면1 버튼2로 지정 
        self.grid_rowconfigure(0, weight=2) # 수식 표시창
        self.grid_rowconfigure(1, weight=1) # 결과 표시창
        for i in range(2, Application.ROW - 2):
            self.grid_rowconfigure(i, weight=2) # 버튼 영역 가중치

    def createDisplay(self):
        # 수식이 표시될 메인 디스플레이 & 결과 디스플레이 (Entry)
        self.display_main = ttk.Entry(self, font=("Helvetica", 30), justify='right', state='readonly')
        self.display_main.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        self.display_result = ttk.Entry(self, font=("Helvetica", 12), justify='right', state='readonly')
        self.display_result.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')

    def createButton(self):
        # 버튼들을 담을 프레임 생성
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.grid(row=2, column=0, columnspan=4, rowspan=4, sticky='nsew')

        # 버튼 프레임 내부의 행과 열도 동적으로 크기 조절되도록 설정
        # 가중치 동일 = 동일 비율
        for i in range(Application.COLUMN):
            self.buttonFrame.grid_columnconfigure(i, weight=1)
        for i in range(Application.ROW - 2):
            self.buttonFrame.grid_rowconfigure(i, weight=1)

        # 버튼 생성
        buttons = [
            ['(', ')', 'C', 'DELETE'],
            ['%', '^', 'SQRT', 'PREV'],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '', '=', '+']
        ]

        for r_idx, row_val in enumerate(buttons):
            for c_idx, col_val in enumerate(row_val):
                # 버튼 클릭 시의 이벤트 지정 (숫자, 연산자면 입력하고 특수키는 특수기능)
                button_command = lambda v=col_val: self.onClickEvent(v)
                button = ttk.Button(self.buttonFrame, text=col_val, command=button_command)
                button.grid(row=r_idx, column=c_idx, padx=5, pady=5, sticky='nsew')

    def onClickEvent(self, value):
        """
        버튼 클릭 시 호출되는 함수
        """
        self.display_main.config(state='normal')
        self.display_result.config(state='normal')
        # C == 전부 지우기
        if value == 'C':
            self.display_main.delete(0, END)

        # DELETE == 한개만 지우기
        # 마지막 입력값을 확인하고 해당 개수만큼 지우기
        elif value == 'DELETE':
            text = self.display_main.get()
            # 없을 경우 무시
            if len(text) < 1:
                pass
            # 연산자일 경우
            if len(text) > 1 and self.display_main.get()[-1] == ' ':
                self.display_main.delete(len(self.display_main.get()) - 2, END)
            # PREV일 경우
            elif len(text) >= 4 and self.display_main.get()[-4:] == 'PREV':
                self.display_main.delete(len(self.display_main.get()) - 4, END)
            # 숫자일 경우
            else:
                self.display_main.delete(len(self.display_main.get()) - 1, END)
        
        # '=' == 계산 실행
        elif value == '=':
            # display_main에서 현재 표현식 가져오기
            expression = self.display_main.get()
            if len(expression.strip()) == 0:
                self.display_result.delete(0, END)
                self.display_result.insert(0, "0")
            else:
                try:
                    result = self.calculator.calculate(calculator.Precedence.to_postfix(expression))
                    
                    # 서브 디스플레이에 계산 과정 표시
                    self.display_result.delete(0, END)
                    self.display_result.insert(0, result)
                    
                except Exception as e:
                    # 계산 중 오류 발생 시 "Error" 표시
                    print(e)
                    self.display_result.delete(0, END)
                    self.display_result.insert(0, "Error")
                
        # 연산자 == 한칸씩 공백 넣고 입력 (파싱 위해서)
        elif value in Application.OPERATORS:
            self.display_main.insert(END, ' ' + value + ' ')

        # 숫자 == 값 추가
        else:
            self.display_main.insert(END, value)

        self.display_main.config(state='readonly')
        self.display_result.config(state='readonly')

    def mainloop(self):
        # 현재 크기를 가져옴
        self.update()
        # 창 생성 위치를 좌측 상단으로 고정
        self.geometry(self.geometry().split('+')[0] + "+0+0")
        return super().mainloop()


if __name__ == "__main__":
    Application().mainloop()