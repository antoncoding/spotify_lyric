import spotipy
import spotipy.util
import time
from os import system
from crawlers.GeniusCrawler import GeniusCrawler
# from crawlers.QQCrawler import QQCrawler
from const import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USERNAME

cache_last_play = None
NON_PLAYING_TIMEOUT = 5
SCOPE = 'user-read-currently-playing'        

def print_lyric(lines):
    for line in lines:
        print(line)

if __name__ == '__main__':
    worker = GeniusCrawler()
    
    token = spotipy.util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    if not token:
        print("Can't get token for", USERNAME)
        exit()

    while True:
        try:
            time.sleep(3)
            sp = spotipy.Spotify(auth=token)
            current_song = sp.currently_playing()
            if current_song is None:
                print('No song')
                time.sleep(NON_PLAYING_TIMEOUT)
                continue
            
            if current_song['item'] == cache_last_play:
                continue

            cache_last_play = current_song['item']
            artist = current_song['item']['artists'][0]['name']
            name_song = current_song['item']['name']
            
            try:
                print('\nSong: {}\nArtist: {}'.format(name_song, artist))
                _ = system('clear')
                
                lines = worker.search_for_lyrics(artist, name_song)
                print_lyric(lines)
            
            except AttributeError as e:
                cache_last_play = current_song['item']
                print('No Lyric Found: {}'.format(name_song))
                continue
        
        except KeyboardInterrupt:
            exit()
        
        except spotipy.client.SpotifyException: 
            print('get new access token')
            token = spotipy.util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    