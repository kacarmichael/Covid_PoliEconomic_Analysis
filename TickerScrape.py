import pandas as pd
import numpy as np
import os

import re

os.chdir(r'****')

url = "https://finviz.com/screener.ashx"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path=r'****', log_path=r'****')
driver.set_page_load_timeout(600)

driver.get(url)

sector_list = driver.find_element_by_id("fs_sec")
options = sector_list.find_elements_by_tag_name("option")

#First entry is "Any", last is "Custom"
options = options[1:-1]
sector_text = []
for option in options:
    sector_text.append(option.get_attribute("value"))

#Adjust list in case of errors
sector_text = sector_text[6:11]

df = pd.DataFrame(columns = ['symbol', 'company_name', 'sector', 'industry'])
for sector in sector_text:
    c_sector = sector
    url = "https://finviz.com/screener.ashx?v=111&f=sec_" + sector
    driver.get(url)
    ind_list = driver.find_element_by_id("fs_ind")
    ind_options = ind_list.find_elements_by_tag_name("option")
    ind_options = ind_options[1:-1]
    ind_text = []
    for industry in ind_options:
        ind_text.append(industry.get_attribute("value"))
    for industry in ind_text:
        c_industry = industry
        r = 1
        url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,ind_"+industry+",sec_"+sector+"&r="+str(r)
        driver.get(url)
        try: 
            pagination = driver.find_element_by_css_selector("#screener-content > table > tbody > tr:nth-child(7)")
        except:
            print("No conent for industry: {}".format(industry))
            continue
        if len(pagination.find_elements_by_tag_name("b")) == 1:
            print("No pagination detected")
            url_num = 1
        elif len(pagination.find_elements_by_tag_name("a")) > 1:
            num_pages = pagination.find_elements_by_tag_name("a")[-2].text
            url_num = (int(num_pages)-1)+(20*int(num_pages)-1)
        while r <= url_num:
            url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,ind_"+industry+",sec_"+sector+"&r="+str(r)
            driver.get(url)
            table_body = driver.find_element_by_css_selector("#screener-content > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1)")
            table_rows = table_body.find_elements_by_tag_name("tr")[1:]
            for row in table_rows:
                cells = row.find_elements_by_tag_name("td")
                c_symbol = cells[1].text
                c_name = cells[2].text
                new_row = pd.DataFrame(data = {'symbol': c_symbol, 'company_name': c_name, 'sector': c_sector, 'industry': c_industry}, index=[0])
                df = df.append(new_row)
                print("Added Company {} With Symbol {}".format(c_name, c_symbol))
            r += 20

df.to_csv("stocksymbols_2.csv")

#Export symbols as a txt file
data = pd.read_csv("stocksymbols_full.csv")

#Want healthcare, consumercyclical, communicationservices, industrials

sectors = data.loc[data['sector'].isin(['healthcare', 'consumercyclical', 'communicationservices', 'industrials'])]

symbols = sectors['symbol']

symbols.to_csv('symbols.txt', index=False, sep='\n')






