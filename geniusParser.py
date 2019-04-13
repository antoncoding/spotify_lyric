from bs4 import BeautifulSoup
import requests

def search_lyric_from_genius(artist, song):
    _artist = str(artist).strip().replace(' ', '-').replace("'", '')
    _name_song = song.strip().replace(' ', '-').replace("'", '')
    song_url = '{}-{}-lyrics'.format(_artist, _name_song)
    request = requests.get("https://genius.com/{}".format(song_url))

    html_code = BeautifulSoup(request.text, features="html.parser")
    lyric = html_code.find("div", {"class": "lyrics"}).get_text()
    print('From: Genius Lyric')
    for line in lyric.split('\n'):
        if ']' in line or '[' in line: continue
        print(line)
    return True