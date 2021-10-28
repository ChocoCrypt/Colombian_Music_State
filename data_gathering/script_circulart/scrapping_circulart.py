from selenium import webdriver
import pandas as pd
from time import sleep

link = "https://circulart.org/2021/artistas-rueda/"
driver = webdriver.Chrome()
driver.get(link)


not_error = True
index = 1
ids = []
while(not_error):
    try:
        artist_id = driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div/div/div/div/div[{index}]").get_attribute("id")
        index+=1
        ids.append(artist_id)
    except:
        not_error = False

print(len(ids))
total_info  = []
for i in ids:
    artist_url = f"https://circulart.org/2021/portafolio-artista-rueda/?p={i}"
    driver.get(artist_url)
    driver.implicitly_wait(1)
    artist_name = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[1]/div/div/div/h1").text
    artist_description = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[1]/div/div/div/div[2]").text
    artist_gen = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[1]/div/div/div/div[3]").text
    info = {"name":artist_name,
                  "artist_description":artist_description,
                  "generos":artist_gen,
                  "id_circulart":i}
    total_info.append(info)

circulart_data = pd.DataFrame(total_info)
print(circulart_data)
