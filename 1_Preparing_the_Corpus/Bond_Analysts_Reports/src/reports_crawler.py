import reports_crawling_tool as cr
import re

##########################
# 기능 : 파일 이름 전처리
def preprocess_filename(filename):
    text = re.sub(r'[^\w\s]', '', filename)
    text = re.sub(r'[A-Za-z가-힣]', '', text)
    return text


########################
# 기능 :
def get_reports_pdf():
    # 2008-04-10 ~ 2023-10-19 기간에 맞게 설정
    min_reports_num = 10    # 가장 예전 보고서 (url의 번호)
    max_reports_num = 6781  # 가장 최근 보고서 (url의 번호)
    for i in range(min_reports_num, max_reports_num + 1):
        url = f"https://finance.naver.com/research/debenture_read.naver?nid={i}"
        soup = cr.get_soup(url)

        # pdf_file download
        title = soup.select_one('th.view_sbj p.source').get_text(strip=True)
        title = preprocess_filename(title)  # 파일 이름 전처리
        print("title", title)

        pdf_name = title[0:8]
        pdf_name = f'{pdf_name}_{i}'
        print("pdf_name : ", pdf_name)
        folder_path = "./reports_pdf_files"

        # # downloading action
        # try:
        #     url = soup.select_one('th.view_report').find('a')['href']
        # except Exception as e:
        #     print(f'done (error) : {i}')
        #     continue
        # response = requests.get(url)
        # with open('{0}{1}.pdf'.format(folder_path, pdf_name), 'wb') as file:
        #     file.write(response.content)
        print("다운로드 완료!")
