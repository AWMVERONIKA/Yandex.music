from yandex_music import Client
from creds import email, passw
import pprint
import json


client = Client.from_credentials(email, passw)


# GET PLAYLISTS
palylists_info = client.users_playlists_list()

my_playlists_names = []

for playlist_info in palylists_info:
    playlist_owner = playlist_info.to_dict()['owner']['login']
    playlist_owner_id = playlist_info.to_dict()['owner']['uid']
    playlist_id = playlist_info.to_dict()['kind']
    playlist_name = playlist_info.to_dict()['title']
    my_playlists_names.append(playlist_name)

    # print(f'{playlist_name}, playlist owner: {playlist_owner}, playlist_owner_id: {playlist_owner_id}, playlist_id: {playlist_id}')


# CREATE PLAYLIST IF NOT EXISTS
new_playlist_name = 'my_new_playlist'

if new_playlist_name not in my_playlists_names:
    client.users_playlists_create(title=new_playlist_name, visibility='private')
else:
    pass


# SEARCH TRACKS
searching_track = client.search('Alpine Uneverse Organika')


# FETCHING TRACK NAME AND ID
track_data = searching_track['best']['result']
album_id = track_data['albums'][0].to_dict()['id_']
track_artist = track_data['artists'][0].to_dict()['name']
track_name = track_data.to_dict()['title']
track_id = track_data.to_dict()['id_']

# print(f'{track_artist} - {track_name}, track id: {track_id}, album_id: {album_id}')


# DOWNLOAD TRACK
# client.users_likes_tracks()[0].fetch_track().download(filename='demo', codec='mp3', bitrate_in_kbps=320)


# TRACK DEMO
link_to_track_demo = client.tracks_download_info(track_id='37540625', get_direct_links=True)[0].to_dict()['direct_link']


# ADD TRACK TO LIKED SONGS
# client.users_likes_tracks_add(track_ids='37540625') # this action also turned off 'do not recommend' mark


# ADD TRACK TO SPECIFIC PLAYLIST
palylists_info = client.users_playlists_list()[1]
playlist_revision = palylists_info.to_dict()['revision'] # request every time before inserting track to playlist
# client.users_playlists_insert_track(kind=1005, track_id=37540625, album_id=4761432, at=10, revision=playlist_revision) # kind -> playlist id, at -> position to insert, revision -> requered for every playlist update


# TRACKS IN LIKED SONGS
user_liked_songs_json = client.users_likes_tracks().to_dict()

all_liked_tracks_list = user_liked_songs_json['tracks'][0:10]

liked_songs = []

for info in all_liked_tracks_list:
    track_id = info['id_']
    track_info = client.tracks(info['id_'])
    track_type = track_info[0].to_dict()['type_']
    if track_type == 'music': # need to pass by podcasts in the playlist
        track_artist = track_info[0].to_dict()['artists'][0]['name']
        track_name = track_info[0].to_dict()['title']
        liked_songs.append(f'{track_artist} - {track_name}, track id: {track_id}')
    else:
        pass

# print(liked_songs)


# TRACKS IN SPECIFIC PLAYLIST
playlist = client.users_playlists(1005)

playlist_tracks_info = playlist['tracks']

playlist_songs = []

for song in playlist_tracks_info:
    track_id = song.to_dict()['id_']
    track_info = client.tracks(song.to_dict()['id_'])
    track_type = track_info[0].to_dict()['type_']
    if track_type == 'music': # need for bypass podcasts in a playlist
        track_artist = track_info[0].to_dict()['artists'][0]['name']
        track_name = track_info[0].to_dict()['title']
        playlist_songs.append(f'{track_artist} - {track_name}, track id: {track_id}')
    else:
        pass

# print(playlist_songs)