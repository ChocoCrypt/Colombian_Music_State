from selenium import webdriver
from tqdm import tqdm
import pandas as pd


driver = webdriver.Chrome()
driver.get("https://www.last.fm/es/tag/colombia/artists?page=1")
driver.implicitly_wait(1)
last_page = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[5]/div[3]/div/div[1]/nav/ul/li[8]/a").text
last_page = int(last_page)
last_page = 2


last_fm_data = []
for page_number in tqdm(range(1,last_page+1)):
    driver.get(f"https://www.last.fm/es/tag/colombia/artists?page={page_number}")
    for i in range(1,30):
        try:
            artist_name = driver.find_element_by_xpath(f"/html/body/div[5]/div[2]/div[5]/div[3]/div/div[1]/section/ol/li[{i}]/div/h3/a").text
            data = {"name":artist_name}
            lastfm_data.append(artist_name)
        except:
            pass

lastfm_data = pd.DataFrame(full_data)
driver.close()




colombia_scene_list = []


#añado los datos del dataframe que hice de lastfm
for i in tqdm(lastfm_data):
    data = {"name":i,
            "lugar_extraido":"lastfm"}
    colombia_scene_list.append(data)

print(colombia_scene_list)
