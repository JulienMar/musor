import configparser

import os
import pylast
import requests
import pygn
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TCON, TDRC

config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config['DEFAULT']['API_KEY']
API_SECRET = config['DEFAULT']['API_SECRET']
CLIENT_ID = config['DEFAULT']['CLIENT_ID']
USER_ID = config['DEFAULT']['USER_ID']


class Musor:
    def set_album_names(directory, album, artist):
        tracks = Musor.get_tracks(artist, album)
        realtracks = os.listdir(directory)
        for track in tracks:
            for realTrack in realtracks:
                if track.title in realTrack:
                    number = tracks.index(track)
                    genre = Musor.get_genres(artist, album)
                    file_path = os.path.realpath(realTrack)
                    year = Musor.get_date(artist, album)
                    Musor.set_track_metadata(file_path, artist, track.title, number, album, genre, year)
                    os.rename(file_path, track.title)

        os.rename(directory, os.path.dirname(os.path.abspath(directory))+ "/" + album)

    def get_tracks(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album(artist, album)
        return album.get_tracks()

    def get_genres(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        genres = network.get_album(artist, album).get_top_tags(5)
        all_genres = TCON.GENRES
        list_in_genres = list(filter((lambda genre: genre[0].name.title in all_genres), genres))
        return list_in_genres

    #TODO: find why it returns none
    def get_date(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        year = network.get_album(artist, album).get_release_date()
        print(year)
        return 0

    def set_track_metadata(file, artist, title, number, album_name, genres, year):
        audio = ID3(file)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TPE2"] = TPE2(encoding=3, text=artist)
        #TODO: change to all artist
        audio["TALB"] = TALB(encoding=3, text=album_name)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TCON"] = TCON(encoding=3, text=genres)
        audio["TDRC"] = TDRC(encoding=3, text=year)
        audio["TRCK"] = TRCK(encoding=3, text=number)
        audio.save()

    def test_date(artist, album):
        params = {
            "method": "album.getInfo",
            "album": album,
            "artist": artist,
            'api_key': API_KEY}
        r = requests.get('http://ws.audioscrobbler.com/2.0/', params=params)
        print(r.content)

gnmetadata = pygn.search(CLIENT_ID,USER_ID,'Netsky', 'Netsky')
print(gnmetadata)