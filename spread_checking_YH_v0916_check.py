# import packages
import pandas as pd
import telegram
from datetime import datetime
import time
import sys
import schedule
import os
import pyautogui

########################################################################################################################
# 초기 세팅

# 텔레그램 메신저 봇 설정
bot = telegram.Bot(token='5391323792:AAG0OcPVjmGIh8GKUGSoeGq98VGIw26psSM')
# ETF spread 채널 chat id 확인
# https://api.telegram.org/bot5391323792:AAG0OcPVjmGIh8GKUGSoeGq98VGIw26psSM/getUpdates
chat_id = "-638640292"

# 오늘 날짜 지정
today = datetime.today().strftime('%Y-%m-%d')

# 사용 목적에 따른 경로지정
os.chdir("C:/Users/check/Desktop/spread/Check_ETF_Spread")


########################################################################################################################

# 함수 선언
# 텔레그램 메신저로 스프레드 발송
def notification(text):
    bot.sendMessage(chat_id=chat_id, text=text)


# 09시 00분에 시작 <-- 고민
def start_code():
    bot.sendMessage(chat_id=chat_id, text="# " + today + " #")
    bot.sendMessage(chat_id=chat_id, text="@@ LP 호가 제출 의무 시작 @@")


# 16시 00에 종료
def exit_code():
    print("장 마감으로 인한 스프레드 점검 종료")
    bot.sendMessage(chat_id=chat_id, text="@@ LP 호가 제출 의무 종료 @@")
    sys.exit()  # 프로그램 종료


# 체크 데이터 업데이트 실행 --> 마우스 좌표설정을 통한 수동 업데이트
'''
check expert excel manager: Point(x=1678, y=1057)
설치(refresh 버튼): Point(x=1367, y=555)
설치 확인: Point(x=1638, y=785)
print('current mouse position: ', pyautogui.position())
'''
def refresh_check():
    pyautogui.moveTo(1678, 1057)
    pyautogui.click()
    pyautogui.moveTo(1367, 555)
    pyautogui.click()
    pyautogui.moveTo(1638, 785)
    pyautogui.click()
    time.sleep(20)
    os.system('start excel.exe ETF_LP_spread.xlsm')


########################################################################################################################
# Start code

refresh_check()  # 엑셀파일 업데이트 오류시 실행

time.sleep(30)

#start_code()  # 처음한번만 실행

schedule.every().day.at("15:20").do(exit_code)  # 15시 20분에 종료

while True:
    schedule.run_pending()

    etf_list = pd.read_excel("ETF_LP_spread.xlsm", header=5)

    for i in range(len(etf_list)):
        if etf_list['ask1'][i] == 0 or etf_list['bid1'][i] == 0:
            print('매수/ 매도호가 없음')

            code_o = etf_list['code'][i]
            name_o = etf_list['name'][i]
            ask_o = etf_list['ask1'][i]
            bid_o = etf_list['bid1'][i]

            now_time = "[" + time.strftime('%H:%M:%S') + "]" + "\n"
            message_o = "현재 호가 없음" + "\n"
            warr = name_o + "(A" + str(code_o) + ")" + "\n"
            spread_value = "매도: " + str(ask_o) + " " + "매수: " + str(bid_o) + "\n"

            ask_bid = now_time + message_o + warr + spread_value
            notification(ask_bid)

            print(ask_bid)

        elif etf_list['check'][i] == "Y":
            code_y = etf_list['code'][i]
            name_y = etf_list['name'][i]
            ask_y = etf_list['ask1'][i]
            bid_y = etf_list['bid1'][i]
            gap_y = etf_list['gap'][i]
            spread_y_1 = round(etf_list['spread'][i], 4) * 100
            spread_y = round(spread_y_1, 2)
            criterion_y = etf_list['criterion'][i] * 100

            now_time = "[" + time.strftime('%H:%M:%S') + "]" + "\n"
            warr = name_y + "(A" + str(code_y) + ")" + "\n"
            spread_value = "매도: " + str(ask_y) + " " + "매수: " + str(bid_y) + " " + "차이: " + str(gap_y) + "\n"
            spread_mgt = "- 관리 스프레드: " + str(criterion_y) + "%" + "\n"
            spread_now = "- 현재 스프레드: " + str(spread_y) + "%"

            spread_send = now_time + warr + spread_value + spread_mgt + spread_now

            print("스프레드 위반")
            print(spread_send)

            notification(spread_send)

    print("------------------------------------------")

    time.sleep(295)
    print(time.strftime('%H:%M:%S'))
