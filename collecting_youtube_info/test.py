
from youtubesearchpython import VideosSearch
import json
import pandas as pd
from time import sleep
import os
import librosa
from sklearn.decomposition import PCA
import pprint


def grab_10_songs(artist_name):
    videosSearch = VideosSearch(artist_name, limit = 1) #ACA SE DECIDE LA CANTIDAD DE CANCIONES POR ARTISTA
    result = videosSearch.result()
    urls = []
    for i in result["result"]:
        pprint.pprint( i )
        ide = i["id"]
        url = f"https://www.youtube.com/watch?v={ide}"
        urls.append(url)
    return(urls)


grab_10_songs('Shakira')
