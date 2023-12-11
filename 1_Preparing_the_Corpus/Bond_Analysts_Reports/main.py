from reports_crawler import get_reports_pdf
from reports_pdf_tool import get_pdf_text

folder_path = "./reports_pdf_files"

# get_reports_pdf(folder_path)   # 1. pdf 다운로드

get_pdf_text(folder_path)   # 2. text 추출

