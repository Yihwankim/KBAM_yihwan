import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import warnings
from slacker import Slacker
import websocket
import time
import os

# slack 메세지 발송함수

def notification(message):
    token = 'xoxp-437607546230-436145006131-435530691200-2bf72d02dd66ead4465dc399887edbb7'
    slack = Slacker(token)
    slack.chat.post_message('etf', message)


os.chdir("C:/work/spread-monitor")

etf_list = pd.read_excel("KBSTARETF_list_1101.xlsx")


# 스프레드 데이터 기록을 위한 데이터프레임 생성
spread_daily_data = pd.DataFrame({"time_no":[],"code":[],"name":[],"ask":[], "bid":[], "diff_1":[], "SP":[], "check_1":[]},
                      columns = ["time_no","code","name","ask", "bid", "diff_1", "SP", "check_1"])

index_count = 0

while True:

    def spread_check(code):

        warnings.simplefilter('ignore')    

        #code = input("CODE : ")
        
        
        # 크롤링 데이터의 정제를 위한 함수        

        def cleartext(text):
            text = text.replace("\n"," ").replace("\t","").replace("\r","").replace(",","").replace("\xa0","").strip(" ")
            return text
        
        
        # 네이버금융페이지에서 종목코드 기준으로 ETF별 호가데이터를 가져옴

        url = "https://finance.naver.com/item/sise.nhn?code={}&asktype=5".format(code)

        response = requests.get(url)

        html = BS(response.text, 'html.parser')

        table = html.find_all("table", {"cellspacing":"0"})
                
        # span 태그의 "tah p11 nv01" 은 매도호가, "tah p11 red 01"은 매수호가.
        # 각 5개의 매도호가, 매수호가를 가져옴

        span_list_ask = table[1].find_all("span", {"class":"tah p11 nv01"})
        span_list_bid = table[1].find_all("span", {"class":"tah p11 red01"})

        span_list_ask_1 = []
        span_list_bid_1 = []

        #print("ask", span_list_ask)
        #print("bid", span_list_bid)
        
                
        for i in range(len(span_list_ask)):

            if cleartext(span_list_ask[i].text) != "":

                if i % 2 != 1:

                    continue

                span_list_ask_1.append(int(cleartext(span_list_ask[i].text)))

        for i in range(len(span_list_bid)):

            if cleartext(span_list_bid[i].text) != "":

                if i % 2 != 0:

                    continue

                span_list_bid_1.append(int(cleartext(span_list_bid[i].text)))



        #print(span_list_ask_1)
        #print(span_list_bid_1)
        
        # 최우선 매도호가/매수호가, 호가차이, 스프레드등을 계산함

        first_ask = int(min(span_list_ask_1))
        first_bid = int(max(span_list_bid_1))
        diff = first_ask-first_bid
        spread = round(diff / ((first_ask+first_bid)/2)*100,4)
                
        return code, first_ask, first_bid, diff, spread
    
    
    # 각 ETF별로 스페레드 위반 여부 체크
    # PC화면에 종목코드, 종목명, 스프레드, 현재 시간 출력
    
    for i in range(len(etf_list)):
        
        index_count =index_count + 1
        
        check = 0
    
        etf_code = etf_list['code2'][i]

        a = spread_check(etf_code)

        now_time = time.strftime('%H:%M:%S')
    
        #print(etf_list['name'][i], now_time)
        #print(a)
        #print(" ")
    
        warr = str(etf_code) +"  "+ etf_list['name'][i]+"  "+ "SP : "+ str(a[4]) + "  "+ now_time
        spread_value = "매도: " + str(a[1]) + " " + "매수: "+ str(a[2]) +" "+"차이: " + str(a[3])
        # spread_value1 = "매도: {}  매수: {}  차이: {}".format(str(a[1]), str(a[2]), str(a[3])) 
        
        print(warr)
        
        # ETF의 신고스프레드를 float형태의 값으로 읽어옴
        b = float(etf_list['spread'][i])
        # print(b)
        
        
        # ETF의 신고스프레드의 위반여부 체크, 위반시 "스프레드위반"출력 및 slack메신저로 메세지 발송 
                
        if float(a[4]) > b:
            
            check = 1
                        
            print("스프레드위반")
            notification(warr)
            notification(spread_value)
        
        
        # 스프레드 데이터를 데이터 프레임형태로 순차적으로 삽입
        # time_no : 생성시간, code: 종목코드, name:종목명, ask:매도호가, bid:매수호가, diff_1:호가차이, SP:스프레드, check_1:위반여부        
        
        time_no = now_time
        code = str(etf_list['code2'][i])
        name = str(etf_list['name'][i])
        ask = int(a[1])
        bid = int(a[2])
        diff_1 = int(a[3])
        SP = a[4]
        check_1 = check
        
        #print(time_no, code, name, ask, bid, diff_1, SP, check_1)
        spread_daily_data.ix[index_count] = [time_no, code, name, ask, bid, diff_1, SP, check_1]
            
            
    print("------------------------------------------")
    
    # 스프레드 데이터 프레임을 엑셀파일로 저장
    spread_daily_data.to_excel("./daily_data/spread_daily_data_1106.xlsx")
    
    time.sleep(300)
    