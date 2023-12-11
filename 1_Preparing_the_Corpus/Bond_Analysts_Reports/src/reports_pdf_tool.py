from PyPDF2 import PdfReader
import reports_utility_module as util
import pandas as pd
import os
import re


######################################
# 기능 : 폴더 내의 pdf 파일의 text를 추출한다.
@ util.timer_decorator
def get_pdf_text(folder_path):
    # 폴더 내의 모든 PDF 파일 목록을 가져옴
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_data = []

    error_count = 0

    # 각 PDF 파일에 대해 텍스트 추출
    for pdf_file in pdf_files:
        try:
            file_path = os.path.join(folder_path, pdf_file)
            text = ""
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                num_pages = len(reader.pages)
                # text 추출
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text += page.extract_text()

            text = util.preprocess_text(text)                # text 전처리
            date = util.format_date(pdf_file[:8])    # 파일 이름에서 날짜 얻음
            print("date : ", date)                      # 날짜 출력
            print(f"Text from {pdf_file}:\n{text}\n")   # 추출된 텍스트 출력 (또는 다른 처리)

            # pdf의 데이터 추가
            new_row = [date, text]
            pdf_data.append(new_row)
        except Exception as e:
            print(e)
            error_count += 1

    print("len pdf_data :", len(pdf_data))
    print("error_count :", error_count)

    df_pdf_data = pd.DataFrame(pdf_data, columns=['date', 'text'])
    csv_file_path = f"./reports_text.csv"
    df_pdf_data.to_csv(path_or_buf=csv_file_path, encoding="utf-8", index=False)
