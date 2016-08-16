# Musor

Script to automatically add metadata (ID3 tags) to music files.

##Setup

Install mutagen with pip.
Register a developper account on https://developer.gracenote.com/.
Add a new app.
Make config file with USER_ID and CLIENT_ID as values.
Run pygn.register(clientid), this returns a user id.
Fill in the correct values in config file.

##Use

The main method you should use is set_album_names(directory, album, artist).
This will do all the work.
