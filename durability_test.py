import tkinter as tk
from datetime import datetime

# 텍스트 파일명
TEXT_FILENAME = "durability_test_data.txt"

# 데이터 저장 함수
def save_data_to_text(data):
    with open(TEXT_FILENAME, "a") as file:
        file.write(data + "\n")

# 테스트 시작 시간 읽어오는 함수
def read_start_time():
    try:
        with open(TEXT_FILENAME, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                if line.startswith("테스트 시작 시간:"):
                    return line.split(": ")[1].strip()
    except FileNotFoundError:
        return None

# 테스트 시작 시간 저장 함수
def save_start_time():
    try:
        global start_time
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        save_data_to_text(f"테스트 시작 시간: {start_time_str}")
        label_start_time.config(text=f"시작 시간:\n{start_time_str}", font=("TkDefaultFont", 10, "bold"))
        label_result.config(text="테스트가 시작되었습니다.", foreground="green")
        update_timer()  # 시작 시간부터 현재까지의 경과 시간을 업데이트하기 위해 타이머를 시작합니다.
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")

# 테스트 정지 시간 저장 함수
def save_stop_time():
    try:
        global start_time, timer_id
        stop_time = datetime.now()
        stop_time_str = stop_time.strftime("%Y-%m-%d %H:%M:%S")
        label_stop_time.config(text=f"정지 시간:\n{stop_time_str}", font=("TkDefaultFont", 10, "bold"))
        start_time_str = read_start_time()
        if start_time_str:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            elapsed_time = stop_time - start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_time_str = f"{hours}시간 {minutes}분 {seconds}초"
            save_data_to_text(f"테스트 정지 시간: {stop_time_str}")
            save_data_to_text(f"작동 시간: {elapsed_time_str}")
            moves = elapsed_time.seconds // 12  # 12초로 나눈 값을 이동 횟수로 지정
            save_data_to_text(f"이동 횟수: {moves}")
            label_result.config(text="테스트가 정지되었습니다.", foreground="green")
            save_data_to_text("-" * 100)  # 구분선 추가
            window.after_cancel(timer_id)  # 타이머를 중지합니다.
        else:
            label_result.config(text="시작 시간이 없습니다.", foreground="red")
    except PermissionError:
        label_result.config(text="파일이 열려 있거나 쓰기 권한이 없습니다.", foreground="red")


# 타이머 업데이트 함수
def update_timer():
    global timer_id
    now = datetime.now()
    elapsed_time = now - start_time
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_str = f"{hours}시간 {minutes}분 {seconds}초"
    label_timer.config(text=f"경과 시간: {elapsed_time_str}")
    # 1000ms마다 업데이트
    timer_id = window.after(1000, update_timer)

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("Durability Test Recorder")
window.geometry("320x250+100+100")

# 결과 표시 레이블
label_result = tk.Label(window, text="")
label_result.grid(row=3, column=0, columnspan=2, pady=5)

# 시작 시간 표시 레이블
label_start_time = tk.Label(window, text="", font=("TkDefaultFont", 10))
label_start_time.grid(row=4, column=0, columnspan=2, pady=5)

# 정지 시간 표시 레이블
label_stop_time = tk.Label(window, text="", font=("TkDefaultFont", 10))
label_stop_time.grid(row=5, column=0, columnspan=2, pady=5)

# 타이머 표시 레이블
label_timer = tk.Label(window, text="경과 시간: 0시간 0분 0초")
label_timer.grid(row=6, column=0, columnspan=2, pady=5)

# 테스트 시작 버튼
button_start = tk.Button(window, text="테스트 시작", command=save_start_time)
button_start.grid(row=7, column=0, padx=5, pady=(10, 20), sticky="ew")

# 테스트 정지 버튼
button_stop = tk.Button(window, text="테스트 정지", command=save_stop_time)
button_stop.grid(row=7, column=1, padx=5, pady=(10, 20), sticky="ew")

# 버튼과 메시지 중앙 정렬
window.grid_rowconfigure(7, weight=1)
window.grid_columnconfigure((0, 1), weight=1)

window.mainloop()
