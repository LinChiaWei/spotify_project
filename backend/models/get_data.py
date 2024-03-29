import spotipy
import spotipy.util as util
from models.get_token import get_token
import time
import requests as rq


def find_songs_name(items):
    last50songs = []
    for i in range(len(items)):
        data = []
        current_track = items[i]['track']
        time = items[i]['played_at']
        album = current_track['album']
        album_name = album['name']
        album_image_inf = album['images'][1]
        album_image_url = album_image_inf['url']
        artist_inf = album['artists']
        artist_name = artist_inf[0]['name']
        artist_uri = artist_inf[0]['uri'].split(":", 2)[2]

        t = trans_time(time)
        # print(str(t))

        data.append(current_track['name'])
        data.append(artist_name)
        data.append(album_image_url)
        data.append(t)
        data.append(artist_uri)
        last50songs.append(data)

    return last50songs
    
def take_second(list):
    return list[3]

def trans_time(t):
    t = t.split('T')
    date = t[0]
    time = t[1].split('.')[0]
    return date+" "+time

def get_artist_genres(artist_id,headers):
    URL = 'https://api.spotify.com/v1/artists/{}'.format(artist_id)
    output = rq.get(URL,headers=headers).json()
    return output['genres']


def get_data():

    token = get_token()
    headers = {"Authorization": "Bearer {}".format(token['access_token'])}

    sp = spotipy.client.Spotify(headers)
    data = sp.current_user_recently_played(50)

    items =  data['items']

    last50songs = find_songs_name(items)

    for song in last50songs[:]:
        song[-1] = get_artist_genres(song[-1],headers=headers)

    return last50songs

def count_song(data):
    song_count = {}
    song_list = []
    for song in data:
        # print(song)
        song_name = song[0]
        artist_name =  song[1]
        song_image_url = song[2]
        if song_name in song_count:
            continue
        else:
            song_count.setdefault(song_name,[])
            song_count[song_name].append(0)
            song_count[song_name].append(artist_name)
            song_count[song_name].append(song_image_url)

    for song in data:
        song_name = song[0]
        song_count[song_name][0] +=1

    for item in song_count:
        dic = {}
        dic['SongName'] = item
        dic['Artist'] = song_count[item][1]
        dic['Cover'] = song_count[item][2]
        dic['Count'] = song_count[item][0]
        data = [item, song_count[item][1] ,song_count[item][2],song_count[item][0]]
        song_list.append(data)

    song_list.sort(key=take_second,reverse=True)
    
    return song_list


def get_user_info():
    token = get_token()
    headers = {"Authorization": "Bearer {}".format(token['access_token'])}
    sp = spotipy.client.Spotify(headers)
    user = sp.me()
    l = []
    l.append(user['display_name'])
    l.append(user['images'][0]['url'] )

    return l
    






    
