import pandas as pd
import numpy as np
import os

import re

os.chdir(r'C:\Users\Aaron\Google Drive\School Stuff\Summer 2020\Project')

url = "https://finviz.com/screener.ashx"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path=r'C:\Users\Aaron\Desktop\Gecko\geckodriver.exe', log_path=r'C:\Users\Aaron\Desktop\Gecko\geckodriver.log')
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

"""
test_df = pd.DataFrame(columns = ['symbol', 'company_name', 'sector', 'industry'])
test_sector = "basicmaterials"
#No pagination
#test_industry = 'agriculturalinputs'
#Pagination
test_industry = 'specialtychemicals'
test_r = 1
test_url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,ind_"+test_industry+",sec_"+test_sector+"&r="+str(test_r)
driver.get(test_url)
test_pagination = driver.find_element_by_css_selector("#screener-content > table > tbody > tr:nth-child(7)")
#Detects if there is no pagination
if len(test_pagination.find_elements_by_tag_name("b")) == 1:
    print("No pagination detected")
    test_url_num = 1
elif len(test_pagination.find_elements_by_tag_name("a")) > 1:
    test_num_pages = test_pagination.find_elements_by_tag_name("a")[-2].text
    test_url_num = (int(test_num_pages)-1)+(20*int(test_num_pages)-1)
while test_r <= test_url_num:
    test_url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,ind_"+test_industry+",sec_"+test_sector+"&r="+str(test_r)
    driver.get(test_url)
    table_body = driver.find_element_by_css_selector("#screener-content > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1)")
    table_rows = table_body.find_elements_by_tag_name("tr")[1:]
    for row in table_rows:
        cells = row.find_elements_by_tag_name("td")
        symbol = cells[1].text
        company_name = cells[2].text
        sector = test_sector
        industry = test_industry
        new_row = pd.DataFrame(data = {'symbol': symbol, 'company_name': company_name, 'sector': sector, 'industry': industry}, index=[0])
        test_df = test_df.append(new_row)
    test_r += 20
"""   

"""
#Export symbols as a txt file
data = pd.read_csv("stocksymbols_full.csv")

#Want healthcare, consumercyclical, communicationservices, industrials

sectors = data.loc[data['sector'].isin(['healthcare', 'consumercyclical', 'communicationservices', 'industrials'])]

symbols = sectors['symbol']

symbols.to_csv('symbols.txt', index=False, sep='\n')
"""





