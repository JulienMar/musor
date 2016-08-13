import configparser

import os
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

    def get_gracenote_album_data(artist, album):
        gnmetadata = pygn.search(CLIENT_ID, USER_ID, artist, album)
        return gnmetadata

    def get_gracenote_track_data(artist, album, track):
        gnmetadata = pygn.search(CLIENT_ID, USER_ID, artist, album, track)
        return gnmetadata

    def get_track_titles(gnmetadata_album):
        tracks = []
        for track in gnmetadata_album['tracks']:
            tracks.append(track['track_title'])
        print(tracks)

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

    def set_track_metadata(file, gracenote_data, track_number):
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


grdat = Musor.get_gracenote_album_data("Netsky", "Netsky")
Musor.get_track_titles(grdat)

