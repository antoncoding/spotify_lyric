from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import urllib.parse
import pylrc
from model_traditional_conversion.langconv import Converter

from crawlers.Crawler import Crawler

class QQCrawler(Crawler):
    def __init__(self):
        super().__init__('QQ Music')

    def isEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def convert_raw_to_uriencoded(self, line, isChineseSong=False):
        if(len(line.split('-')) > 1):
            line = line.split('-')[0]
        encoded = line
        _isChinese = False
        if self.isEnglish(line):
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

    def getSongId(self, artist, song):
        uri_song, isChineseSong = convert_raw_to_uriencoded(song, False)
        uri_artist, _ = convert_raw_to_uriencoded(artist, isChineseSong)
        key = "{song}+{artist}".format(song=uri_song, artist=uri_artist)
        uri = 'http://music.taihe.com/search?key={}'.format(key)
        # parse search result
        request = requests.get(uri)
        html_code = BeautifulSoup(request.text, features="html.parser")
        results = html_code.find("div", {
                                 "class": "search-song-list song-list song-list-hook"}).find("ul").find_all("li")
        sid = json.loads(results[0]['data-songitem'])["songItem"]["sid"]
        return sid

    def getLyticURI(self, sid):
        request_uri = 'http://music.taihe.com/song/{sid}'.format(sid=sid)
        request = requests.get(request_uri)
        html_code = BeautifulSoup(request.text, features="html.parser")
        results = html_code.find("div", {"class": "music-body clearfix"})
        try:
            lyric_link = results.find(
                "div", {"class": "lrc-list pr none"})['data-lrclink']
            return lyric_link
        except:
            return self.raise_not_found()

    def slice_lrc_line(self, line, traditional=True):
        try:
            line = line.split(']')[-1]
            return Converter('zh-hant').convert(line)
        except Exception as e:
            return ' '

    def search_for_lyrics(self, artist, song):
        try:
            sid = self.getSongId(artist, song)
            lyric_link = self.getLyticURI(sid)
            if(lyric_link == False):
                return self.raise_not_found()

            lrc_tuple = urllib.request.urlretrieve(lyric_link)
            lrc_path = lrc_tuple[0]

            lrc_file = open(lrc_path)
            lines = map(
                lambda line: self.slice_lrc_line(line),
                lrc_file.readlines())
            lrc_file.close()
            return list(lines)

        except Exception as e:
            return self.raise_not_found()
