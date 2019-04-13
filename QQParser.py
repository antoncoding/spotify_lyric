from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import urllib.parse
import pylrc
from nltk.corpus import wordnet
from model_traditional_conversion.langconv import Converter

def convert_raw_to_uriencoded(line):
    if not wordnet.synsets(line):
        _simp = Converter('zh-hans').convert(line)
        encoded = urllib.parse.quote(_simp)
        return encoded
    else:
        encoded = '+'.join(line.split(' '))
        return encoded

def getSongId(artist, song):
    uri_artist = convert_raw_to_uriencoded(artist)
    uri_song = convert_raw_to_uriencoded(song)

    uri_song = urllib.parse.quote(song)
    key = "{song}+{artist}".format(song=uri_song, artist=uri_artist)
    uri = 'http://music.taihe.com/search?key={}'.format(key)
    # parse search result
    request = requests.get(uri)
    html_code = BeautifulSoup(request.text, features="html.parser")
    results = html_code.find("div", {"class": "search-song-list song-list song-list-hook"}).find("ul").find_all("li")
    sid = json.loads(results[0]['data-songitem'])["songItem"]["sid"]
    return sid

def getLyticURI(sid):
    request_uri = 'http://music.taihe.com/song/{sid}'.format(sid=sid)
    request = requests.get(request_uri)
    html_code = BeautifulSoup(request.text, features="html.parser")
    results = html_code.find("div", {"class": "music-body clearfix"})
    try:
        lyric_link = results.find("div", {"class": "lrc-list pr none"})['data-lrclink']
        return lyric_link
    except:
        return False
    
def slice_lrc_line(line, traditional=True):
    try:
        line = line.split(']')[-1]
        return Converter('zh-hant').convert(line)
    except Exception as e:
        return ' '

def search_lyric_from_QianQian(artist, song, traditional=True):
    sid = getSongId(artist, song)
    lyric_link = getLyticURI(sid)
    if(lyric_link==False): return False

    lrc_tuple = urllib.request.urlretrieve(lyric_link)
    lrc_path = lrc_tuple[0]

    lrc_file = open(lrc_path)
    lrc_string = ''.join(map(lambda line: slice_lrc_line(line), lrc_file.readlines()) )
    # lrc_string = ''.join(lrc_file.readlines())
    lrc_file.close()
    print(lrc_string)
    return True


if __name__ == '__main__':
    search_lyric('animal', 'maroon 5')

