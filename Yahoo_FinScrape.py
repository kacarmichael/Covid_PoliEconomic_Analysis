import pandas as pd
import numpy as np
import os

import time
from datetime import datetime

os.chdir(r'C:\Users\Aaron\Google Drive\School Stuff\Summer 2020\Project')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs
import requests

symbols = pd.read_csv("symbols.txt", delimiter="\n", header=None, names=['symbol'])


driver = webdriver.Firefox(executable_path=r'C:\Users\Aaron\Desktop\Gecko\geckodriver.exe', log_path=r'C:\Users\Aaron\Desktop\Gecko\geckodriver.log')
driver.set_page_load_timeout(600)

full_df = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low',
                                  'Close*', 'Adj Close**', 'Volume', 'Symbol'])

#Split the list of symbols into 7 groups to mitigate lost progress by errors
#sym_1 = symbols[0:207]
#sym_1 = sym_1[symbols.index[symbols['symbol'] == "LB"].tolist()[0]:len(sym_1)]
#sym_2 = symbols[207:415]
#sym_2 = symbols[symbols.index[symbols['symbol'] == "NLS"].tolist()[0]:415]
#sym_3 = symbols[415:622]
#sym_4 = symbols[622:829]
#sym_5 = symbols[829:1036]
#sym_6 = symbols[1036:1243]
#sym_7 = symbols[1243:1450]
#sym_8 = symbols[1450:1657]
#sym_9 = symbols[1657:1862]

#Some companies were not found at first, this list ties up loose ends
sym_extra = ['BURL', 'ETH', 'AMZN', 'SIC', 'BBBY', 'CULP', 'VCNX', 'OPK', 'WBT', 'WM']

for symbol in sym_extra:
    url = "https://www.finance.yahoo.com/quote/" + symbol + "/history"
    driver.get(url)
    scroll_to_bottom(driver)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0][0:-1]
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[df['Date'] >= '2020-01-01']
    except:
        print("No entry for " + symbol)
        df = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low',
                                  'Close*', 'Adj Close**', 'Volume', 'Symbol'])
    df['Symbol'] = symbol
    full_df = full_df.append(df)
    print("Added " + symbol)

full_df.to_csv("yahoo_fin_extra.csv")

yf1_2 = pd.read_csv("yahoo_fin_1_2.csv")
yf_3 = pd.read_csv("yahoo_fin_3.csv")
yf_4 = pd.read_csv("yahoo_fin_4.csv")
yf_5 = pd.read_csv("yahoo_fin_5.csv")
yf_6 = pd.read_csv("yahoo_fin_6.csv")
yf_7_8 = pd.read_csv("yahoo_fin_7_8.csv")
yf_9 = pd.read_csv("yahoo_fin_9.csv")
yf_extra = pd.read_csv("yahoo_fin_extra.csv")

yahoo_full = yf1_2.append(yf_3).append(yf_4).append(yf_5).append(yf_6).append(
    yf_7_8).append(yf_9).append(yf_extra)

filter = yahoo_full['Open'].str.contains("Dividend")
yahoo_full = yahoo_full[~filter]

yahoo_full.to_csv("yahoo_fin_full.csv")

#Code obtained from https://stackoverflow.com/questions/32391303/how-to-scroll-to-the-end-of-the-page-using-selenium-in-python
def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))








#Testing with amazon and Google
test_symbols = ['AMZN', 'TPCO', "SCHL"]
test_full_df = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low',
                                  'Close*', 'Adj Close**', 'Volume', 'Symbol'])
for symbol in test_symbols:
    test_url = "https://www.finance.yahoo.com/quote/" + symbol + "/history"
    driver.get(test_url)
    scroll_to_bottom(driver)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find_all('table')[0]
    test_df = pd.read_html(str(table))[0][0:-1] #Drop last row
    try:
        test_df['Date'] = pd.to_datetime(test_df['Date'])
        test_df = test_df[test_df['Date'] >= '2020-01-01']
    except:
        print("No entry for " + symbol)
    test_df['Symbol'] = symbol
    test_full_df = test_full_df.append(test_df)

