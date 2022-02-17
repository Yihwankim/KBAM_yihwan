# import packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import telegram
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Kkma, Twitter
from konlpy.utils import pprint
import time
from datetime import datetime, timedelta

# 뉴스검색키워드
key_words = "수소"
stop_words = ["삼중수소", "황화수소"]

# 뉴스검색 url 생성을 위한 변수들
url1 = "https://search.naver.com/search.naver?&where=news&query=" + key_words + "&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=4&"
url2 = "ds=2021.03.24.09.24&de=2021.03.25.09.24"
url3 = "&docid=&nso=so:dd,p:1d,a:all&mynews=0&start="
url4 = "&refresh_start=0"

now = datetime.now()
year = str(now.year)
month = str(now.month)
day = str(now.day)
hour = str(now.hour)
minute = str(now.minute)

start_time = now - timedelta(1)
start_year = str(start_time.year)
start_month = str(start_time.month)
start_day = str(start_time.day)

page_num = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101,
            111, 121, 131, 141, 151, 161, 171, 181, 191, 201,
            211, 221, 231, 241, 251, 261, 271, 281, 291, 301,
            311, 321, 331, 341, 351, 361, 371, 381, 391, 401]

# 뉴스검색 기간
# 최근 1일
start_time = start_year + "." + start_month + "." + start_day + "." + hour + "." + minute
# start_time = year + "." + month + "." + testday + "." + hour_before + "." + minute
end_time = year + "." + month + "." + day + "." + hour + "." + minute

# 뉴스 크롤링
# 뉴스타이틀, 요약내용, 링크주소 저장

data = []

for i in page_num:

    url = url1 + "ds=" + start_time + "&de=" + end_time + url3 + str(i) + url4

    # print(url)
    # print("-------------------")

    html = requests.get(url)

    soup = bs(html.content, 'html.parser')

    li_tmp = soup.find_all('li', {'class': 'bx'})

    # print(li_tmp)

    for i in li_tmp:

        try:

            tit = i.find('a', {'class': 'news_tit'}).text
            # link = i.find('a',{'class':'info'})

            link = i.find_all('a', {'class': 'info'})[1]['href']
            dsc = i.find('div', {'class': 'news_dsc'}).text

            data.append([tit, dsc, link])

            print(link)
            print("--------------------------------")

        except:

            continue

df1 = pd.DataFrame(data, columns=['title', 'text', 'links'])

for i in stop_words:
    df1 = df1[~df1['text'].str.contains(i)]

df1.reset_index(inplace=True)

# 크롤링된 뉴스별 유사도 계산(요약내용기준)
# 꼬꼬마단어장, tf-idf 알고리즘 사용

mydoclist = list(df1['text'])

kkma = Kkma()

doc_nouns_list = []

for doc in mydoclist:

    nouns = kkma.nouns(doc)
    doc_nouns = ''

    for noun in nouns:
        doc_nouns += noun + ' '

    doc_nouns_list.append(doc_nouns)

tfidf_vectorizer = TfidfVectorizer(min_df=1)

tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)

document_distances = (tfidf_matrix * tfidf_matrix.T)

id_result = pd.DataFrame(document_distances.toarray())

# 유사뉴스 제거
# 유사도 0.1이상

set_df = {}

for i in id_result.columns:

    temp_list = []

    for j in id_result.columns:

        # print(id_result[i][j])

        if id_result[i][j] > 0.1:
            temp_list.append(j)

    set_df[i] = temp_list

result = {}

for key, value in set_df.items():

    # print(key)
    # print(value)

    value = [value[0]]

    if value not in result.values():
        result[key] = value

# 텔레그램 메신저로 뉴스 발송
# chat_id는 해당 체널에서 사용하는 아이디
# chat_id는 https://api.telegram.org/bot1700245019:AAGOS77_lGbnrHswTnJ8oYolLgA2mCAR76o/getUpdates 에서 확인

bot = telegram.Bot(token='1700245019:AAGOS77_lGbnrHswTnJ8oYolLgA2mCAR76o')
chat_id = "-1001360969815"

for i in result.keys():
    send_message = df1['links'][i]

    bot.sendMessage(chat_id=chat_id, text=send_message)

    time.sleep(2)










