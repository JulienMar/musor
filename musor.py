import pylast, glob, os
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TCON, TDRC
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config['DEFAULT']['API_KEY']
API_SECRET = config['DEFAULT']['API_SECRET']


class Musor:
    def set_album_names(directory, album, artist):
        tracks = Musor.get_tracks(artist, album)
        for track in tracks:
            print(tracks.index(track) + 1)
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                print(file)
        os.rename(directory, os.path.dirname(os.path.abspath(directory))+ "/" + album)

    def get_tracks(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album(artist, album)
        return album.get_tracks()

    def get_genre(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        genres = network.get_album(artist, album).get_top_tags(5)
        ALL_GENRES = TCON.GENRES
        print(ALL_GENRES)
        for genre in genres:
            if ALL_GENRES.__contains__(genre[0].name.title()):
                print(genre[0].name.title())

    def set_track_metadata(file, artist, title, number, album_name, genre, year):
        audio = ID3(file)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TPE2"] = TPE2(encoding=3, text=artist)
        #TODO: change to all artist
        audio["TALB"] = TALB(encoding=3, text=album_name)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TCON"] = TCON(encoding=3, text=genre)
        audio["TDRC"] = TDRC(encoding=3, text=year)
        audio["TRCK"] = TRCK(encoding=3, text=number)
        audio.save()

Musor.set_album_names("/home/julien/Documents/FunProjects/Netsky", "Netsky", "Netsky")
