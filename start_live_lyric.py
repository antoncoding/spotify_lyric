import spotipy
import spotipy.util
import time
from os import system
from QQParser import search_lyric_from_QianQian
from geniusParser import search_lyric_from_genius
from const import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USERNAME

cach_last_play = None

scope = 'user-read-currently-playing'
token = spotipy.util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

if token:
    while True:
        time.sleep(3)

        sp = spotipy.Spotify(auth=token)
        current_song = sp.currently_playing()
        if type(current_song)=='NoneType': continue
        if current_song['item'] == cach_last_play: continue

        cach_last_play = current_song['item']
        artist = current_song['item']['artists'][0]['name']
        name_song = current_song['item']['name']
        print('\nSong: {}\nArtist: {}'.format(name_song, artist))

        try:
            _ = system('clear')
            success = search_lyric_from_QianQian(artist, name_song)
            if success: continue
            success = search_lyric_from_genius(artist, name_song)
        except:
            cach_last_play = current_song['item']
            print('No Lyric Found: {}'.format(name_song))

else:
    print("Can't get token for", username)
