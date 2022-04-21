# import packages
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import warnings
# from slacker import Slacker
import telegram
import websocket
from datetime import datetime
import time
import sys
import schedule
import os

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
    bot.sendMessage(chat_id=chat_id, text="@@ LP 호가 제출 의무 종료 @@)")
    sys.exit()  # 프로그램 종료


########################################################################################################################
# Start code
start_code()

schedule.every().day.at("16:00").do(exit_code)  # 4시에 종료

while True:
    schedule.run_pending()

    etf_list = pd.read_excel("ETF_LP_spread.xlsm", header=5)

    for i in range(len(etf_list)):
        if etf_list['check'][i] == "Y":
            notification("스프레드 점검 필요")

            code_y = etf_list['code'][i]
            name_y = etf_list['name'][i]
            ask_y = etf_list['ask1'][i]
            bid_y = etf_list['bid1'][i]
            gap_y = etf_list['gap'][i]
            spread_y = round(etf_list['spread'][i], 4)
            criterion_y = etf_list['criterion'][i]

            now_time = time.strftime('%H:%M:%S')
            warr = "* " + name_y + "(A" + str(code_y) + ")" + "  " + now_time
            spread_value = "매도: " + str(ask_y) + " " + "매수: " + str(bid_y) + " " + "차이: " + str(gap_y)
            spread_mgt = "- 관리 스프레드: " + str(criterion_y)
            spread_now = "- 현재 스프레드: " + str(spread_y)

            print("스프레드 위반")
            print(warr)
            print(spread_value)

            notification(warr)
            notification(spread_value)
            notification(spread_mgt)
            notification(spread_now)

    print("------------------------------------------")

    time.sleep(60)