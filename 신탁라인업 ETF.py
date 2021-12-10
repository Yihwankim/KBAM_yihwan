# import packages
import pandas as pd
from selenium import webdriver

########################################################################################################################
# call chrome web-driver
chrome = webdriver.Chrome('chromedriver.exe')

chrome.get('http://asp.wstock2.edaily.co.kr/TrustDeptKB/L0001')

# change the type, name to code
for i in range (5):
    name_type = chrome.find_element_by_css_selector\
        ('#DetailList0' + str(i+2) + 'Ajax > div > table > thead > tr > th:nth-child(2) > select')
    name_type.click()
    option_type = chrome.find_element_by_css_selector\
        ('#DetailList0' + str(i+2) +'Ajax > div > table > thead > tr > th:nth-child(2) > select > option:nth-child(2)')
    option_type.click()


chrome.find_element_by_xpath('/html/body/form/div/div[3]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[15]/td[2]').text
/html/body/form/div/div[3]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[1]/td[2]
/html/body/form/div/div[3]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[14]/td[2]

/html/body/form/div/div[3]/div[2]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[2]
/html/body/form/div/div[3]/div[2]/div/div[1]/div[2]/div/table/tbody/tr[34]/td[2]

/html/body/form/div/div[3]/div[3]/div[1]/div/table/tbody/tr[1]/td[2]
/html/body/form/div/div[3]/div[3]/div[1]/div/table/tbody/tr[27]/td[2]