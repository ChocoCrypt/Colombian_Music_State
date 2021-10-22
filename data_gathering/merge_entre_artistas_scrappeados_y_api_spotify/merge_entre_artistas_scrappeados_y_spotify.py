from spoty import *
from time import sleep
import pandas as pd
from progress.bar import Bar

#login en spotify
id_cliente = 'c12d5ca9e15e433298368cbf94a280a4'
secreto_cliente = '1cb6ec606ac048289a3bff4be7895f29'
spotify = SpotApi(id_cliente,secreto_cliente)
datos = pd.read_csv("nombres_bandas_generados.csv" , index_col = None)
index = 0
final_data_for_analysis = []
#recorro todos los artistas de spotify y busco sus respectiva informacion si esta, si no, la dejo como nula
bar = Bar("progress of merge..." , max = len(datos["name"]))
for i in datos["name"]:
    try:
        real_name = i
        artista = spotify.obtener_artista_nombre(i)
        ide = artista["id"]
        link_spotify = artista["external_urls"]["spotify"]
        followers = artista["followers"]["total"]
        generos = artista["genres"]
        images = artista["images"]
        popularidad = artista["popularity"]
        nombre_en_spotify = artista["name"]
        artist_type = artista["type"]
        lugar_extraido = datos["lugar_extraido"][index]
        index += 1
        bar.next()
    except Exception as e:
        real_name = i
        artista = "not in database"
        ide = "not in database"
        link_spotify = "not in database"
        followers = 0
        generos = "not in database"
        images =  "not in database"
        popularidad = 0
        nombre_en_spotify = "not in database"
        artist_type =  "not in database"
        lugar_extraido = datos["lugar_extraido"][index]
        index += 1
        bar.next()
    #esta es la información que va a tener el dataframe total
    info = {"name_scrapped":i,
            "id":id,
            "link_spotify":link_spotify,
            "followers":followers,
            "generos":generos,
            "imagenes":images,
            "popularidad":popularidad,
            "nombre_en_spotify":nombre_en_spotify,
            "type_of_artist":type,
            "lugar_extraido":lugar_extraido,
            "index_on_last_dataset":index}
    final_data_for_analysis.append(info)

#guardo los datos finales
final_data = pd.DataFrame(final_data_for_analysis)
print(final_data)
final_data.to_csv("final_data.csv")


