from youtubesearchpython import VideosSearch
import os

def grab_10_songs(artist_name):
    videosSearch = VideosSearch(artist_name, limit = 10)
    result = videosSearch.result()
    urls = []
    for i in result["result"]:
        ide = i["id"]
        url = f"https://www.youtube.com/watch?v={ide}"
        urls.append(url)
    return(urls)


def download_10_songs_artist_name(artist_name):
    urls = grab_10_songs(artist_name)
    try:
        dest_folder = os.makedirs(f"artists/{artist_name}")
    except:
        print(f"folder for {artist_name} already exists")
    index = 1
    for i in urls:
        print(f"downloading {index} for {artist_name}")
        os.system(f'youtube-dl -x -i --audio-format mp3 {i} --output   "artists/{artist_name}/{index}.%(mp3)s"   ')
        index += 1

download_10_songs_artist_name("juanes")



