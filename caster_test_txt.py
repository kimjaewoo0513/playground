import tkinter as tk
from datetime import datetime

# 텍스트 파일명
TEXT_FILENAME = "cater_test_data.txt"

# 데이터 저장 함수
def save_data_to_text(data):
    with open(TEXT_FILENAME, "a") as file:
        file.write(data)

# 파일에서 테스트 시작 시간 읽기 함수
def read_start_time():
    try:
        with open(TEXT_FILENAME, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                if "테스트 시작 시간:" in line:
                    start_time_str = line.split(": ")[1].strip()
                    return datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    except FileNotFoundError:
        return None

# 테스트 시작 시간 저장 함수
def save_start_time():
    try:
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        save_data_to_text(f"테스트 시작 시간: {start_time_str}\n")
        label_start_time.config(text=f"시작 시간:\n{start_time_str}", font=("TkDefaultFont", 10, "bold"))
        label_result.config(text="테스트가 시작되었습니다.", foreground="green")
        # 가동 시간 초기화
        update_elapsed_time(reset=True)
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")

# 테스트 정지 시간 저장 함수
def save_stop_time():
    try:
        start_time = read_start_time()
        if start_time:
            stop_time = datetime.now()
            stop_time_str = stop_time.strftime("%Y-%m-%d %H:%M:%S")
            elapsed_time = stop_time - start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_time_str = f"{hours}시간 {minutes}분 {seconds}초"
            save_data_to_text(f"테스트 정지 시간: {stop_time_str}\n")
            save_data_to_text(f"작동 시간: {elapsed_time_str}\n")
            label_stop_time.config(text=f"정지 시간:\n{stop_time_str}", font=("TkDefaultFont", 10, "bold"))
            label_result.config(text="테스트가 정지되었습니다.", foreground="green")
            save_data_to_text("-" * 100 + "\n")  # 구분선 추가
            # 가동 시간 업데이트 멈춤
            window.after_cancel(timer)
        else:
            label_result.config(text="시작 시간이 파일에 기록되어 있지 않습니다.", foreground="red")
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")

# RPM 계산 함수
def mps_to_rpm(mps, diameter):
    try:
        mps = float(mps)
        diameter = float(diameter) / 1000  # mm를 m로 변환
        if mps < 0 or diameter <= 0:
            raise ValueError("속도와 지름은 양의 실수여야 합니다.")
        rpm = (mps / (3.14 * diameter)) * 60
        return f"속도: {mps} m/s, 지름: {diameter * 1000} mm, RPM: {rpm:.2f}"
    except ValueError:
        return "올바른 값을 입력해주세요."

# RPM 변환 함수
def convert_to_rpm(event=None):
    mps = entry_mps.get()
    diameter = entry_diameter.get()
    result = mps_to_rpm(mps, diameter)
    if result.startswith("속도:"):
        label_result.config(text=result, foreground="black")
    else:
        label_result.config(text=result, foreground="red")

# 가동 시간 실시간 업데이트 함수
def update_elapsed_time(reset=False):
    global start_time, timer
    if reset:
        start_time = datetime.now()
    elapsed_time = datetime.now() - start_time
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_str = f"{hours}시간 {minutes}분 {seconds}초"
    label_elapsed_time.config(text="경과 시간: " + elapsed_time_str, foreground="black")
    # 가동 시간 업데이트
    timer = window.after(1000, update_elapsed_time)

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("Caster Test Data Recorder")

# 속도(m/s) 입력 위젯 및 라벨
label_mps = tk.Label(window, text="속도(m/s):")
label_mps.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_mps = tk.Entry(window)
entry_mps.grid(row=0, column=1, padx=10, pady=5)
entry_mps.bind("<Return>", convert_to_rpm)  # 엔터 키를 누르면 변환 작업 수행

# 구동 바퀴 지름(mm) 입력 위젯 및 라벨
label_diameter = tk.Label(window, text="구동 바퀴 지름(mm):")
label_diameter.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_diameter = tk.Entry(window)
entry_diameter.grid(row=1, column=1, padx=10, pady=5)
entry_diameter.bind("<Return>", convert_to_rpm)  # 엔터 키를 누르면 변환 작업 수행

# 변환 버튼
button_convert = tk.Button(window, text="변환", command=convert_to_rpm)
button_convert.grid(row=2, column=0, columnspan=2, pady=10)

# 결과 표시 레이블
label_result = tk.Label(window, text="")
label_result.grid(row=3, column=0, columnspan=2, pady=5)

# 테스트 시작 시간 표시 레이블
label_start_time = tk.Label(window, text="", font=("Helvetica", 11))
label_start_time.grid(row=4, column=0, columnspan=2, pady=5)

# 가동 시간 표시 레이블
label_elapsed_time = tk.Label(window, text="", font=("Helvetica", 11))
label_elapsed_time.grid(row=5, column=0, columnspan=2, pady=5)

# 테스트 정지 시간 표시 레이블
label_stop_time = tk.Label(window, text="", font=("Helvetica", 11))
label_stop_time.grid(row=6, column=0, columnspan=2, pady=5)

# 테스트 시작 버튼
button_start = tk.Button(window, text="테스트 시작", command=save_start_time)
button_start.grid(row=7, column=0, padx=5, pady=(10, 20))

# 테스트 정지 버튼
button_stop = tk.Button(window, text="테스트 정지", command=save_stop_time)
button_stop.grid(row=7, column=1, padx=5, pady=(10, 20))

# Tkinter 루프 시작
window.mainloop()
