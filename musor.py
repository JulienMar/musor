import pylast

API_KEY = "628ab5741348060109a15df6939e138d"
API_SECRET = "513578b1fe1f5cb49b10290b64badc64"


class Musor:
    def musor():
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album("Chet Faker", "Built on Glass")

        for track in album.get_tracks():
            print(track)



Musor.musor()