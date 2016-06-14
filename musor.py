import pylast
from mutagen.id3 import ID3, TPE1

API_KEY = "628ab5741348060109a15df6939e138d"
API_SECRET = "513578b1fe1f5cb49b10290b64badc64"


class Musor:
    def set_album_names():
        return 0

class LastfmData:
    def get_tracks(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album(artist, album)
        return album

class Metadata:
    def __init__(self):
        

    def set_title_metadata(file, artist):
        audio = ID3(file)
        audio.add(TPE1(encoding=3, text="netsky"))
        audio.save()

    def set_track_metadata(self):
Musor.set_title_metadata("/home/julien/Documents/FunProjects/album1/Escape.mp3", "Netsky")