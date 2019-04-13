from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import urllib.parse
import pylrc
from model_traditional_conversion.langconv import Converter

# from nltk.corpus import wordnet
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def convert_raw_to_uriencoded(line, isChineseSong=False):
    if(len(line.split('-'))>1): line = line.split('-')[0]
    encoded = line
    _isChinese = False
    if isEnglish(line):
        if isChineseSong:
            # Only get first name of the Singer
            encoded = line.split(' ')[0]
        else:
            encoded = '+'.join(line.split(' '))
    else:
        _simp = Converter('zh-hans').convert(line)
        encoded = urllib.parse.quote(_simp)
        _isChinese = True
    return encoded, _isChinese
        

def getSongId(artist, song):
    uri_song, isChineseSong = convert_raw_to_uriencoded(song, False)
    uri_artist, _ = convert_raw_to_uriencoded(artist, isChineseSong)
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
    lrc_file.close()
    print('From: 千千音樂')
    print(lrc_string)
    return True


if __name__ == '__main__':
    search_lyric_from_QianQian('Eric Chou','我爱过你')

