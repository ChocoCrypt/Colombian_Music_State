import spoty as s
import pandas as pd
import re
from pprint import pprint


id_cliente = "39d1a630f0d046c597d469c50e28a976"
secreto_cliente = "cf77cfd0c5c449ac9010f55f35145228"
camino_a_los_artistas = "./final_data.csv"


def main():

    print("Entered Main")

    api = s.SpotApi(id_cliente=id_cliente, secreto_cliente=secreto_cliente)
    csv = pd.read_csv(camino_a_los_artistas)
    los_capos =  zip(csv['name_scrapped'],csv['link_spotify'])
    completica = pd.DataFrame(
        columns=[
            "artist_id",
            "id",
            "popularity",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
            "time_signature",
        ]
    )



    for name,url in los_capos:
        try:
            print(f'{name:<8}: inicia proceso de extracción de datos')
            _id = re.search(r"https://open.spotify.com/artist/([A-Za-z0-9-]+)", url)[1]
            completica = completica.append(api.datos_canciones_artistas(_id, completica), ignore_index=True)
            print(completica.tail())
        except TypeError as e:
            print(f'{name} no tiene cuenta en spotify')
            print(f"{e}")

    comps_opts = dict(method="zip", archive_name="completica.csv")
    completica.to_csv(path_or_buf="completica.zip", index=False, compression=comps_opts)


if __name__ == "__main__":
    main()
