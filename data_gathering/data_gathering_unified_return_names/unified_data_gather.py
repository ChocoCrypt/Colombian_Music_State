#!/usr/bin/env python3
import json
from tqdm import tqdm
from time import sleep
from selenium import webdriver
import pandas as pd



print("Processing SIMUS")
#SIMUS
datos_simus = pd.read_excel("bandas_simus.xls")



#BOMM
print("Processing Bomm")
#crea una session de un driver de google chrome
driver = webdriver.Chrome()
bomm_artist_url = "https://www.bogotamusicmarket.com/Artistas?year=2021"
driver.get(bomm_artist_url)
#espera 1 segundo para que el driver seguro cargue la página
sleep(1)
not_done = True
bomm_list = []
while(not_done):
    #agarro todos los nombres de una pagina específica
    for i in (range(1,17)):
        #si no se puede agarrar el elemento es porque no hay mas bandas
        try:
            first_artist = driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/div[2]/div/div[{i}]/figure/figcaption/h4/a")
            name = first_artist.text
            data = {"band_name":name}
            bomm_list.append(data)
        except:
            not_done = False
            break
    try:
        #voy a la siguiente pagina, y hago esto hasta que no haya mas artistas
        next_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div[3]/div/a")
        next_button.click()
        sleep(1)
    except:
        driver.close()

bomm_data = pd.DataFrame(bomm_list)


print("PROCESSING CIRCULART")
#CIRCULART
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

total_info  = []
#voy a cortar los ids un poquito para ver que pasa
for i in tqdm(ids):
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
driver.close()



print("PROCESSING LASTFM")
#LASTFM


driver = webdriver.Chrome()
driver.get("https://www.last.fm/es/tag/colombia/artists?page=1")
driver.implicitly_wait(1)
last_page = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[5]/div[3]/div/div[1]/nav/ul/li[8]/a").text
last_page = int(last_page)

lastfm_data = []
for page_number in tqdm(range(1,last_page+1)):
    driver.get(f"https://www.last.fm/es/tag/colombia/artists?page={page_number}")
    for i in range(1,30):
        try:
            artist_name = driver.find_element_by_xpath(f"/html/body/div[5]/div[2]/div[5]/div[3]/div/div[1]/section/ol/li[{i}]/div/h3/a").text
            data = {"name":artist_name}
            lastfm_data.append(artist_name)
        except:
            pass

driver.close()




print("PROCESSING FAMOUS STUFF")
#CANTANTES FAMOSOS
with open("famous_data.json") as file:
    data = json.load(file)
famous_dataframe = pd.DataFrame(data)






print("UNIFYING EVERYTHING")
#UNIFY EVERITHING


colombia_scene_list = []



#añado los datos del dataframe que hice de lastfm
for i in lastfm_data:
    data = {"name":i,
            "lugar_extraido":"lastfm"}
    colombia_scene_list.append(data)

#añado los datos del dataframe que hice de famosos previamente
for i in famous_dataframe["name"]:
    data = {"name":i,
            "lugar_extraido":"pagina_artistas_famosos"}
    colombia_scene_list.append(data)

#añado los datos de circulart
for i in circulart_data["name"]:
    data = {"name":i,
            "lugar_extraido":"circulart"}
    colombia_scene_list.append(data)
#añado los datos del dataframe que hice de BOMM previamente
for i in bomm_data["band_name"]:
    data = {"name":i,
            "lugar_extraido":"bomm"}
    colombia_scene_list.append(data)

#añado los datos que descargue del SIMUS
for i in datos_simus["Nombre"]:
    data = {"name":i,
            "lugar_extraido":"simus"}
    colombia_scene_list.append(data)

colombia_state_names = pd.DataFrame(colombia_scene_list)
colombia_state_names.to_csv("nombres_bandas_generados.csv")
print("Everything run correctly")
