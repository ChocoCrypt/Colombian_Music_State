from selenium import webdriver
import pandas as pd
from time import sleep


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
    for i in range(1,17):
        #si no se puede agarrar el elemento es porque no hay mas bandas
        try:
            first_artist = driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/div[2]/div/div[{i}]/figure/figcaption/h4/a")
            name = first_artist.text
            data = {"band_name":name}
            bomm_list.append(data)
        except:
            not_done = False
            print("done")
            break
    try:
        #voy a la siguiente pagina, y hago esto hasta que no haya mas artistas
        next_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div[3]/div/a")
        next_button.click()
        sleep(1)
    except:
        print("ya no hay click")
        driver.close()

bomm_data = pd.DataFrame(bomm_list)
print(bomm_data)
