import configparser

import os
import pygn
import re
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TCON, TDRC

config = configparser.ConfigParser()
config.read("config.ini")

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
        return tracks

    def set_album_names(directory, album, artist):
        gnmetadata_album = Musor.get_gracenote_album_data(album, artist)
        tracks = Musor.get_track_titles(gnmetadata_album)

        final_directory = os.path.expanduser(directory)
        all_music_files = os.listdir(final_directory)

        for track in tracks:
            for music_file in all_music_files:
                check_track_name = re.sub(r'\W+', '', track).lower()
                check_music_file = re.sub(r'\W+', '', music_file).lower()
                if check_track_name in check_music_file:
                    print(music_file)
                    gn_track_data = Musor.get_gracenote_track_data(artist, album, track)
                    Musor.set_track_metadata(final_directory + '/' + music_file, gn_track_data)
                    extension = music_file.rsplit('.', 1)[-1]
                    #os.rename(file_path, final_directory + "/" + track + "." + extension)

        os.rename(directory, os.path.dirname(os.path.abspath(directory)) + "/" + album)

    def set_track_metadata(file, gracenote_data):
        audio = ID3(file)
        audio["TIT2"] = TIT2(encoding=3, text=gracenote_data['track_title'])
        audio["TPE2"] = TPE2(encoding=3, text=gracenote_data['track_artist_name'])
        audio["TALB"] = TALB(encoding=3, text=gracenote_data['album_title'])
        audio["TPE1"] = TPE1(encoding=3, text=gracenote_data['album_artist_name'])
        genres = [value['TEXT'] for key, value in gracenote_data['genre'].items()]
        audio["TCON"] = TCON(encoding=3, text=genres)
        audio["TDRC"] = TDRC(encoding=3, text=gracenote_data['album_year'])
        audio["TRCK"] = TRCK(encoding=3, text=gracenote_data['track_number'])
        audio.save()

Musor.set_album_names(os.path.expanduser('~/Documents/FunProjects/Netsky'), 'Netsky', 'Netsky')

