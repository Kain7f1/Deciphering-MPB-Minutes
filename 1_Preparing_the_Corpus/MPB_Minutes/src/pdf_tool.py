from PyPDF2 import PdfReader
import os
import re
import pandas as pd
import utility_module as util

##########################
# 기능 : 날짜 정규식 패턴과 일치하면, 날짜를 YYYY-MM-DD 형태로 리턴한다
def get_date(match):
    if match:
        year, month, day = match.groups()
        # YYYY-MM-DD 형식으로 포맷 변경
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    else:
        return None


#####################################
# 기능 : 의사록에서 날짜를 추출한다 : 정규 표현식을 사용하여 YYYY-MM-DD 형식의 날짜 추출
def extract_formatted_date(text):
    # 의사록에서 나타나는 날짜 패턴
    match_1 = re.search(r"(\d{4}) (\d{1,2}) (\d{1,2})", text)
    match_2 = re.search(r"(\d{4})년(\d{1,2})월(\d{1,2})일", text)
    match_3 = re.search(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일", text)
    match_4 = re.search(r"(\d{4}) 월 일 목(\d{1,2})\s+(\d{1,2})", text)

    match_list = [match_1, match_2, match_3, match_4]
    for match in match_list:
        date = get_date(match)
        if date is not None:    # 일치하는 패턴이 있으면, 날짜 리턴
            return date
    return None                 # 없으면 None 리턴


######################################
# 기능 : 폴더 내의 pdf 파일의 text를 추출한다.
@ util.timer_decorator
def get_pdf_text(folder_path):
    # 폴더 내의 모든 PDF 파일 목록을 가져옴
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_data = []

    non_count = 0

    # 각 PDF 파일에 대해 텍스트 추출
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        text = ""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            # text 추출
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        text = text.replace("\n", "")   # 줄바꿈 제거
        date = extract_formatted_date(text)
        print(f"Text from {pdf_file}:\n{text}\n")   # 추출된 텍스트 출력 (또는 다른 처리)
        print(date)
        if date is None:
            non_count += 1
        new_row = [date, text]
        pdf_data.append(new_row)

    print("len pdf_data : ", len(pdf_data))
    print("non_count : ", non_count)

    df_pdf_data = pd.DataFrame(pdf_data, columns=['date', 'text'])
    csv_file_path = f"./minutes_text.csv"
    df_pdf_data.to_csv(path_or_buf=csv_file_path, encoding="utf-8", index=False)
