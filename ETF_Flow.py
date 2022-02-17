import xlwings as xw
import pyautogui
import time
import os
import datetime
import schedule

def auto():
    os.chdir(r'\\10.206.101.81\23_Multi\03_ETF\01_Report\13_ETF Daily(Flow, Performance)')
    # 마우스 매크로 (데이터 가이드 자동 실행)
    pyautogui.moveTo(565,1059)
    pyautogui.click()
    time.sleep(15)
    pyautogui.moveTo(994,607)
    pyautogui.click()
    time.sleep(15)
    pyautogui.moveTo(994,607)
    pyautogui.click()
    # VBA 실행 및 저장
    path = r"\\10.206.101.81\23_Multi\03_ETF\01_Report\13_ETF Daily(Flow, Performance)"
    wb = xw.Book(path+"\ETF 투자주체별 Flow_1123_auto.xlsm")
    macro = wb.macro('Refresh_dg')
    macro()
    sheet = wb.sheets['투자주체별']
    date = sheet.range('I2').value
    current_work_dir = os.getcwd()
    pdf_path = os.path.join(current_work_dir, "ETF 투자주체별 Flow_{:%y%m%d}.pdf".format(date))
    report_sheet = wb.sheets[0]
    report_sheet.api.ExportAsFixedFormat(0, pdf_path)
    wb.save("ETF 투자주체별 Flow_{:%y%m%d}.xlsm".format(date))
    wb.close

schedule.every().day.at("08:07").do(auto)

while True:
    schedule.run_pending()
    time.sleep(1)