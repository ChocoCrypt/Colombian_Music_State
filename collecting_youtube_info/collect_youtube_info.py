from youtubesearchpython import VideosSearch
import json
import pandas as pd
from time import sleep
import os
import librosa
from sklearn.decomposition import PCA


#este metodo descarga una lista de canciones desde youtube
def descargar_canciones_desde_nombre_youtube(artist_name):
    original_name = artist_name
    urls = grab_10_songs(original_name)
    if(len(urls)>=1):
        try:
            dest_folder = os.makedirs(f"artists/{artist_name}")
        except:
            print(f"folder for {artist_name} already exists")
        index = 1
        for i in urls:
            print(f"downloading {index} for {original_name}")
            os.system(f'youtube-dl -x -i --audio-format mp3 {i} --output   "artists/{artist_name}/{artist_name}{index}.%(mp3)s"   ')
            index += 1
    else:
        print("no hubo canciones")


#este metodo hay que dejarlo asi como está pero hay que cambiar que no se puedan descargar canciones de mas de 10 minutos
def grab_10_songs(artist_name):
    videosSearch = VideosSearch(artist_name, limit = 2) #ACA SE DECIDE LA CANTIDAD DE CANCIONES POR ARTISTA
    result = videosSearch.result()
    urls = []
    for i in result["result"]:
        ide = i["id"]
        duracion = i["duration"]
        duracion_lista = duracion.split(":")
        segundos = 0
        try:
            segundos += int(duracion_lista[-1])
        except:
            segundos += 0
        try:
            segundos += int(duracion_lista[-2])*60
        except:
            segundos += 0
        try:
            segundos += int(duracion_lista[-3])*3600
        except:
            segundos += 0
        print(segundos)
        if(segundos < 600):
            url = f"https://www.youtube.com/watch?v={ide}"
            urls.append(url)
        else:
            print("la cancion es muy larga")
    return(urls)


def get_resume_of_file(filepath):
 #reading files with librosa
    samples,sampling_rate = librosa.load(filepath)
    #creating spectrogram
    sgram = librosa.stft(samples)
    #generating mel spectrogram
    sgram_mag , _ = librosa.magphase(sgram)
    mel_scale_sgram = librosa.feature.melspectrogram(S=sgram_mag , sr = sampling_rate)
    #re scaling mel pectrograms with PCA
    pca = PCA(n_components = 2)#    IMPORTANTE QUE ACA SE DECIDE CUANTOS VECTORES VAMOS A TENER
    pca.fit(mel_scale_sgram)
    values = pca.singular_values_
    print(values)
    return(values)


def resume_folder_into_one_single_file(folder_path , out_name):
    a_name = out_name
    mypath = f"{folder_path}/"
    onlyfiles = [f"{mypath}{f}" for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    inp = ""
    fil = ""
    n = 0
    for i,f in enumerate(onlyfiles):
        inp += f" -i {f}"
        fil += f"[{i}:0]"
        n = i
    cmd = f"""ffmpeg {inp[1:]} -filter_complex '{fil}concat=n={n+1}:v=0:a=1[out]' -map '[out]' {mypath}{a_name}.mp3"""
    os.system(cmd)
    for f in onlyfiles:
        os.system(f"rm {f}")

def resume_10_songs_by_an_artist(artist_name):
    alfabeto = [chr(i) for i in range(ord("A") , ord("Z")+1)]
    alfabeto += [chr(i) for i in range(ord("a") , ord("z")+1)]
    original_name = artist_name
    new_artist_name = ""
    #hago este swap para no tener problemas con caracteres ascii
    for i in artist_name:
        if(i in alfabeto):
            new_artist_name += i
    artist_name = new_artist_name
    print(artist_name)
    #esto que está aca hay que reemplazarlo un metodo que descargue directamente las canciones desde spotify, si no, ahi si de youtube
    descargar_canciones_desde_nombre_youtube(original_name)
    #hay que hacer un try porque puede no haber canciones
    try:
        resume_folder_into_one_single_file(f"artists/{artist_name}", f"{artist_name}_unified")
        valores = get_resume_of_file(f"artists/{artist_name}/{artist_name}_unified.mp3")
        #esto toca esperar antes de borrar porque si no el system se corre paralelo con el os.remove
        #toca borrarlos con el system
        sleep(1)
        os.system(f"rm artists/{artist_name}/{artist_name}_unified.mp3") #ACA BORRO LAS CANCIONES PARA PODERLO CORRER EN MI SERVIDOR
        os.system(f"rm -r artists/{artist_name}") #ACA BORRO LA CARPETA PARA NO HACER SPAM
        info = {"artist":original_name,
                "x1":str(valores[0]),
                "x2":str(valores[1])}
        return(info)
    #esto puede pasar si no habia canciones
    except:
        info = {"artist_name":original_name,
                "x1":str(0),
                "x2":str(0)
                }


def agarrar_toda_la_lista(datos):
    data = pd.read_csv(datos)
    total_data = []
    for i in data["name_scrapped"][0:2]:
        info = resume_10_songs_by_an_artist(i)
        total_data.append(info)
        #hay que poner este sleep para que sigan corriendo los siguientes
        print("preparando el siguiente")
        sleep(1)
    return(total_data)



datos = agarrar_toda_la_lista("final_data.csv")
#with open("vectores_artistas.json" , "w") as file:
#    json.dump(datos , file)
