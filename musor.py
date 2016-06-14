import pylast
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TCON, TDRC

API_KEY = "628ab5741348060109a15df6939e138d"
API_SECRET = "513578b1fe1f5cb49b10290b64badc64"


class Musor:
    def set_album_names():
        return 0

    def get_tracks(artist, album):
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album(artist, album)
        for track in album.get_tracks():
            print(track.get_tag)

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




#Musor.set_track_metadata("/home/julien/Documents/FunProjects/album1/Escape.mp3", "Netsk", "Escape", "1", "1", "drum and bass", "2010")
Musor.get_tracks("Chet Faker", "Built on glass")