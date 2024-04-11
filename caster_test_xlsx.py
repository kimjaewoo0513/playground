import tkinter as tk
from datetime import datetime
import pandas as pd

# 엑셀 파일명
EXCEL_FILENAME = "test_data.xlsx"
# 초기 시트 이름 설정
sheet_name = "Sheet1"

# 엑셀 파일이 있는지 확인하고 데이터 불러오기
try:
    time_records = pd.read_excel(EXCEL_FILENAME)
except FileNotFoundError:
    time_records = pd.DataFrame(columns=["시작 시간", "정지 시간", "작동 시간"])

def update_current_time():
    global sheet_name  # 전역 변수로 선언
    now = datetime.now()
    # 날짜가 바뀌면 새로운 시트 추가
    if now.day != update_current_time.last_day:
        update_current_time.last_day = now.day
        update_current_time.current_sheet += 1
        sheet_name = f"Sheet{update_current_time.current_sheet}"
        time_records.to_excel(EXCEL_FILENAME, sheet_name=sheet_name, index=False)
    window.after(1000, update_current_time)  # 1초마다 업데이트
update_current_time.last_day = datetime.now().day
update_current_time.current_sheet = 0

def save_start_time():
    try:
        now = datetime.now()
        time_records.loc[len(time_records)] = [now, None, None]
        time_records.to_excel(EXCEL_FILENAME, sheet_name=sheet_name, index=False)
        label_result.config(text="시작 시간이 기록되었습니다.", foreground="green")
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")

def save_stop_time():
    try:
        now = datetime.now()
        start_time = time_records.iloc[-1, 0]
        elapsed_time = now - start_time
        # 작동 시간을 시, 분, 초로 변환
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_records.iloc[-1, 1] = now
        time_records.iloc[-1, 2] = f"{hours}시간 {minutes}분 {seconds}초"
        time_records.to_excel(EXCEL_FILENAME, sheet_name=sheet_name, index=False)
        label_result.config(text="정지 시간이 기록되었습니다.", foreground="green")
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")

def mps_to_rpm(event=None):
    try:
        mps = float(entry_mps.get())
        wheel_diameter = float(entry_diameter.get()) / 1000  # mm를 m로 변환
        if mps < 0 or wheel_diameter <= 0:
            raise ValueError("올바른 값을 입력해주세요.")
        rpm = (mps / (3.14 * wheel_diameter)) * 60
        label_result.config(text=f"{rpm:.2f} RPM")
        label_result.config(foreground="black")  # 결과 메시지 색상을 기본값으로 설정
    except ValueError:
        label_result.config(text="올바른 값을 입력해주세요.", foreground="red")  # 오류 메시지를 빨간색으로 표시

    # 항상 현재 날짜와 시간 표시
    update_current_time()

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("m/s to RPM")

# RPM 계산기 레이블
label_rpm_calculator = tk.Label(window, text="RPM 계산기")
label_rpm_calculator.grid(row=0, column=0, columnspan=2, pady=10)

# m/s 입력 위젯 및 라벨
label_mps = tk.Label(window, text="속도(m/s):")
label_mps.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_mps = tk.Entry(window)
entry_mps.grid(row=1, column=1, padx=10, pady=5)
entry_mps.bind("<Return>", mps_to_rpm)  # 엔터 키를 누르면 변환 작업 수행

# 구동 바퀴 지름 입력 위젯 및 라벨
label_diameter = tk.Label(window, text="구동 바퀴 지름(mm):")
label_diameter.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_diameter = tk.Entry(window)
entry_diameter.grid(row=2, column=1, padx=10, pady=5)
entry_diameter.bind("<Return>", mps_to_rpm)  # 엔터 키를 누르면 변환 작업 수행

# 변환 버튼
button_convert = tk.Button(window, text="변환", command=mps_to_rpm)
button_convert.grid(row=3, column=0, columnspan=2, pady=(20, 20))  # 위쪽 여백을 20, 아래쪽 여백을 10으로 설정

# 선 추가
line = tk.Frame(window, height=1, width=200, bg="black")
line.grid(row=4, column=0, columnspan=2)

# 결과 표시 레이블
label_result = tk.Label(window, text="")
label_result.grid(row=5, column=0, columnspan=2, pady=5)

# 테스트 시작 버튼
button_start = tk.Button(window, text="테스트 시작", command=save_start_time)
button_start.grid(row=6, column=0, padx=5, pady=(10, 20))  # 위쪽 여백을 10, 아래쪽 여백을 20으로 설정

# 테스트 정지 버튼
button_stop = tk.Button(window, text="테스트 정지", command=save_stop_time)
button_stop.grid(row=6, column=1, padx=5, pady=(10, 20))  # 위쪽 여백을 10, 아래쪽 여백을 20으로 설정

# 초기에 한 번 표시
update_current_time()

window.mainloop()
