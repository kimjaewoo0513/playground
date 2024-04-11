import os
import pandas as pd

target_folder = os.path.normpath(r'C:\Users\floatic-j\Desktop\Dlody 안정성 테스트\240307\원본\새 폴더')
files_list = os.listdir(target_folder)

for file_name in files_list:
    if file_name.endswith('.csv'):
        csv_path = os.path.join(target_folder, file_name)
        df_new = pd.read_csv(csv_path, encoding="cp949")
        xlsx_file = os.path.splitext(file_name)[0] + '.xlsx'
        xlsx_path = os.path.join(target_folder, xlsx_file)

        df_new.to_excel(xlsx_path, index=False)
        print(f"Converted '{file_name}' to '{xlsx_file}'")