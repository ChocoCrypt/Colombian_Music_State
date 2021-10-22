from selenium import webdriver
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import json

driver  = webdriver.Chrome()
driver.get("https://www.ranker.com/list/bands-from-colombia/reference")
input("already scrolled")
content = driver.page_source
names = []
for i in range(1,142):
    try:
        name = driver.find_element_by_xpath(f"/html/body/div[1]/article/div[3]/div[1]/ul/li[{i}]/div/div/div/h2/a").text
        print(name)
        data = {"name":name}
        names.append(data)
    except:
        pass

with open("famous_data.json" , "w") as file:
    json.dump(data, file)


