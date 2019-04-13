import spotipy
import spotipy.util
import time
from os import system
from QQParser import search_lyric_from_QianQian
from geniusParser import search_lyric_from_genius
from const import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USERNAME

cach_last_play = None
NON_PLAYING_TIMEOUT = 60

scope = 'user-read-currently-playing'
token = spotipy.util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

if token:
    while True:
        time.sleep(3)

        sp = spotipy.Spotify(auth=token)
        current_song = sp.currently_playing()
        if type(current_song)=='NoneType':
            time.sleep(NON_PLAYING_TIMEOUT)
            continue
        if current_song['item'] == cach_last_play: continue

        cach_last_play = current_song['item']
        artist = current_song['item']['artists'][0]['name']
        name_song = current_song['item']['name']
        try:
            print('\nSong: {}\nArtist: {}'.format(name_song, artist))
            _ = system('clear')
            # Try Searching on Qian Qian
            success = search_lyric_from_QianQian(artist, name_song)
            if success: continue
            # Try Searching on Genius Lyric, throw Error if not Found
            success = search_lyric_from_genius(artist, name_song)
        except:
            cach_last_play = current_song['item']
            print('No Lyric Found: {}'.format(name_song))

else:
    print("Can't get token for", username)
