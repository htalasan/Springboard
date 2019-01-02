import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
import requests
import spotipy
import spotipy.util as util

def get_track_ids_from_playlist(playlist_id, token):
    '''Get the track ids from a playlist'''

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=1"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)
    total_num = parsed['total']

    track_ids = []

    # can only get tracks in 100 track batches
    offsets = [x for x in range(0, total_num, 100)]

    for offset in offsets:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit=100"
        headers = {'Authorization': f"Bearer {token}"}
        r = requests.get(url, headers=headers)
        parsed = json.loads(r.text)

        for d in parsed['items']:
            track_ids.append(d['track']['id'])

    return track_ids

def get_track_info(track_id, token):
    """Get basic track information: id, name, artist, album"""

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)

    track_info = {'id': track_id,
                'name': parsed['name'],
                'artist': [d['name'] for d in parsed['artists']],
                'album':parsed['album']['name']}

    return track_info

def get_playlist_tracks_features(playlist_id, token):
    """Get all the tracks' features from a given playlist_id"""
    track_ids = get_track_ids_from_playlist(playlist_id, token)

    playlist_track_features = []

    for id in track_ids:
        track_info = get_track_features(id, token)
        playlist_track_features.append(track_info)

    df = pd.DataFrame.from_dict(playlist_track_features).set_index('id')

    return df

def get_playlist_tracks_info(playlist_id, token):
    """Get all the tracks' information from a given playlist_id"""

    track_ids = get_track_ids_from_playlist(playlist_id, token)

    playlist_track_info = []

    for id in track_ids:
        track_info = get_track_info(id, token)
        playlist_track_info.append(track_info)

    df = pd.DataFrame.from_dict(playlist_track_info).set_index('id')

    return df

def get_df_from_playlist(playlist_id, token):
    """This returns a merged df with the track info and features of a playlist"""

    df_info = get_playlist_tracks_info(playlist_id, token)
    df_features = get_playlist_tracks_features(playlist_id, token)

    merged = df_info.merge(df_features, on='id')

    return merged

def get_track_name(track_id, token):
    '''Get the track name from a track_id'''

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)

    return parsed['name']

def get_track_artists(track_id, token):
    '''Get the track name from a track_id'''

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)

    return [d['name'] for d in parsed['artists']]

def get_track_features(track_id, token):
    '''Get the audio features for a track'''

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)

    return parsed

def get_track_analysis(track_id, token):
    '''Get the audio analysis for a track'''

    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)

    return parsed


"""
def get_token():
    '''Automatically gets a token'''

    # TODO: Figure the redirect url stuff
    scope = "user-read-private user-read-email user-read-playback-state user-read-currently-playing"
    client_id = 'f17b47d72114409596dba6dbe65a18ab'
    client_secret = '7d6dfb034c74464ea1a4b033252ef002'
    redirect_uri = '???'

    token = util.prompt_for_user_token('nannerpeel', scope, client_id, client_secret, redirect_uri)

    return token
"""
