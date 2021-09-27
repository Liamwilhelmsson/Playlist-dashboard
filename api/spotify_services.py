from rest_framework import status
from requests import post, get, put
import urllib.parse
from .auth_services import get_token_or_none, is_spotify_authenticated
import math

# Spotify API endpoints
SPOTIFY_URL = 'https://api.spotify.com/v1'


def execute_spotify_api_request(session_id, endpoint, method):
    ''' Makes a request to 'https://api.spotify.com/v1/{endpoint} '''

    is_spotify_authenticated(session_id)
    token = get_token_or_none(session_id)

    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + token.access_token }

    print(SPOTIFY_URL + endpoint)
    if method == "GET":
        response = get(SPOTIFY_URL + endpoint, headers=headers)
    elif method == "GET":
        response = post(SPOTIFY_URL + endpoint, headers=headers)
    elif method == "GET":
        response = put(SPOTIFY_URL + endpoint, headers=headers)
    
    try:
        return response.json()
    except:
        return response


def get_spotify_playlists(json): 
    '''
    Gets playlists from the given account and returns a list of the playlist with the following information: 
    {
        id: Spotify identifier for the playlist
        name: Name of playlist
        icon: Playlist icon url 
    }
    '''

    # Get name, id, and icon for each playlist and add it to 
    playlists = json['items']
    playlist_data = []
    for playlist in playlists:
        # Add icon if exists
        icon = playlist['images'][0]['url'] if len(playlist['images']) != 0 else ''
        data = {
            'id': playlist['id'],
            'name': playlist['name'],
            'icon': icon
        }
        playlist_data.append(data)

    return playlist_data


def get_tracks(session_id, playlist_id):
    '''  Gets an array of tracks from the given playlist_id '''

    # Create query string and parse it 
    query = "items(track(id,name,artists(name, id),album(name,images,release_date)))"
    fields = urllib.parse.quote(query)

    tracks = []
    offset = 0
    # Loop the fetch of tracks since limit is 100
    while True: 
        response = execute_spotify_api_request(session_id, f"/playlists/{playlist_id}/tracks?fields={fields}&offset={offset}", "GET")
    
        if 'error' in response:
            return {'error': response['error']['message'], 'status': response['error']['status']}
        elif 'items' not in response:
            return {'error': 'No content', 'status': status.HTTP_204_NO_CONTENT}

        # Extend tracks array with the new tracks 
        tracks = tracks + response['items']
        if len(response['items']) < 100: 
            break 
        
        offset = offset + 100

    # Remove inital track field: {track: {name, album: {}, artist{}, ...}} -> {name, album {}, artists{}, ...}
    tracks = [track['track'] for track in tracks]

    return tracks


def get_track_info(tracks):
    ''' Processes all tracks and returns a list of the following track information:
    {
        id: Playlist id
        trackName: Name of the track
        artistName: Comma seperated string of the artists
        albumName: Album name
        albumCover: url to album cover 
    }
    '''

    track_info_list = []
    for track in tracks:
        # Get artists 
        track_info = {
            'id': track['id'], 
            'trackName': track['name'],
            'artistName': get_artist_names(track, comma_seperated_string=True),
            'albumName': track['album']['name'],
            'albumCover': track['album']['images'][0]['url'] if len(track['album']['images']) != 0 else ''
        }
        track_info_list.append(track_info)

    return track_info_list
 
 
def get_tracks_per_decade(tracks):
    ''' Returns numbers of tracks for each decade 
    {
        name: The decade
        average: The number of tracks in that decade
    }
    '''

    decades_count_dict = {}
    for track in tracks: 
        if track['album']['release_date']: 
            release_year = track['album']['release_date'][0:4]
            release_decade = math.floor(int(release_year)/10) * 10
            decades_count_dict[release_decade] = decades_count_dict.get(release_decade, 0) + 1

    # Sort by decade 
    decades_count_dict = {k: v for k, v in sorted(decades_count_dict.items(), reverse = True)}
    decades_count_list = []
    for decade in decades_count_dict: 
        tracks_per_decade = {
            'name': decade,
            'tracks': decades_count_dict.get(decade),
        }
        decades_count_list.append(tracks_per_decade)

    return decades_count_list


def get_artist_count(tracks):
    ''' Returns dict of the artist and the number of appereances:
    {
        name: Artist name
        tracks: Number of tracks they appeared on 
    }
    '''

    artist_count_dict = {}
    for track in tracks:
        for artist in track['artists']:
            artist_count_dict[artist['name']] = artist_count_dict.get(artist['name'], 0) + 1

    # Sort after number of appereance descending order
    artist_count_dict = {k: v for k, v in sorted(artist_count_dict.items(), key=lambda item: item[1], reverse = True)}

    artist_count_list = []
    others = 0; 
    for artist in artist_count_dict: 
        number_of_appereances = artist_count_dict.get(artist)
        # If total number of tracks are less than 0.33 percent 
        if number_of_appereances <= len(tracks)/300:
            others = others + number_of_appereances; 
        else:
            artist_appearence = {
                'name': artist,
                'tracks': number_of_appereances
            }
            artist_count_list.append(artist_appearence)

    # Add others to list
    if others: 
        artist_count_list.append({'name': "Others", 'tracks': others})

    return artist_count_list


def get_artist_names(track, comma_seperated_string=False):
    ''' Returns list of artists on the given track as either list or comma seperated string '''

    artist_names = []    
    for artist in track['artists']:
        artist_names.append(artist['name'])

    if comma_seperated_string:
        return ", ".join(artist_names)
    else: 
        return artist_names
    

def get_artist_ids(track):
    ''' Returns list of artist ids for one track'''

    artist_ids = []    
    for artist in track['artists']:
        if artist['id']:
            artist_ids.append(artist['id'])

    return artist_ids
    

def get_artists(session_id, tracks): 
    ''' Returns list of all artists for several tracks '''

    artist_ids = []
    for track in tracks: 
        artist_ids = artist_ids + get_artist_ids(track)
    
    # Divide in chunks of 50 ids as a comma seperated since the spotify api has a limit of 50 artists
    ids_strings = [",".join(artist_ids[x:x+50]) for x in range(0, len(artist_ids), 50)]

    artists = []
    for ids_string in ids_strings: 
        response = execute_spotify_api_request(session_id, f"/artists?ids={ids_string}", "GET")

        if 'error' in response:
            return {'error': response['error']['message'], 'status': response['error']['status']}
        elif 'artists' not in response:
            return {'error': "No content", 'status': status.HTTP_204_NO_CONTENT}

        artists = artists + response['artists']

    return artists


def get_genre_count(session_id, tracks): 
    ''' Returns dict of the genres and number of tracks it is on :
    {
        name: Genre name
        tracks: Number of tracks that has that genre 
    }
    '''
    artists = get_artists(session_id, tracks)
    
    genres_count_dict = {}
    for artist in artists: 
        if len(artist['genres']):
            genres_count_dict[artist['genres'][0]] =  genres_count_dict.get(artist['genres'][0], 0) + 1

    genres_count_dict = {k: v for k, v in sorted(genres_count_dict.items(), key=lambda item: item[1], reverse = True)}

    genres_count_list = []
    others = 0
    for index, genre in enumerate(genres_count_dict): 
        genre_count = genres_count_dict.get(genre)
        # Only include the 7 largest genres 
        if index >= 7: 
            others = others + genre_count
        else:
            artist_appearence = {
                'name': genre,
                'tracks': genre_count
            }
            genres_count_list.append(artist_appearence)

    # Add others to list
    if others: 
        genres_count_list.append({'name': "Others", 'tracks': others})

    return genres_count_list


def get_audio_features(session_id, tracks): 
    track_ids = []
    for track in tracks: 
        if track['id']:
            track_ids.append(track['id'])
    
    # Divide in chunks of 100 ids as a comma seperated since the spotify api has a limit of 100 audio_features
    ids_strings = [",".join(track_ids[x:x+50]) for x in range(0, len(track_ids), 50)]

    audio_features = []
    for ids_string in ids_strings: 
        response = execute_spotify_api_request(session_id, f"/audio-features?ids={ids_string}", "GET")

        if 'error' in response:
            return {'error': response['error']['message'], 'status': response['error']['status']}
        elif 'audio_features' not in response:
            return {'error': "No content", 'status': status.HTTP_204_NO_CONTENT}

        audio_features = audio_features + response['audio_features']

    return audio_features


def get_bpm_count(audio_features): 
    ''' Returns dict of the bpm and number of tracks with that bpm rounded up or down to closest tenth, i.e 175->180, 174->170
    {
        name: The bpm 
        tracks: Number of tracks with a rounded bpm of the key 
    }
    '''
    
    bpm_dict = {}
    for audio_feature in audio_features: 
        bpm = audio_feature['tempo']
        # All below 70 are counted together and all over 200. 
        if bpm < 70:
            bpm_dict[69] = bpm_dict.get(69, 0) + 1
        elif bpm >= 200: 
            bpm_dict[200] = bpm_dict.get(200, 0) + 1
        else: 
            bpm_rounded = round(bpm / 10) * 10
            bpm_dict[bpm_rounded] = bpm_dict.get(bpm_rounded, 0) + 1

    
    bpm_dict = {k: v for k, v in sorted(bpm_dict.items())}

    bpm_count_list = []
    for bpm in bpm_dict: 
        if bpm < 70: 
            name = "<70"
        elif bpm == 200:
            name = "200<"
        else:
            name = f"{bpm}"

        bpm_count = {
            'name': name,
            'tracks': bpm_dict.get(bpm)
        }
        bpm_count_list.append(bpm_count)

    return bpm_count_list


def get_audio_characteristics_average(audio_features): 
    ''' Returns dict of the average audio characterstics for each of the track: 
    {
        name: Audio characteristic ('danceability', 'energy', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'positivity')
        average: The average of the given characteristic
    }
    '''
    
    audio_characteristics_totals_dict = {}
    audio_characteristics = ['danceability', 'energy', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'valence']
    # Loop to get average for each characterstic 
    for audio_feature in audio_features: 
        for characteristic in audio_characteristics:
            audio_characteristics_totals_dict[characteristic] = audio_characteristics_totals_dict.get(characteristic, 0) + audio_feature[characteristic]

    # Get average for each characterstic
    audio_characteristics_average_dict = {k: v/len(audio_features) for k, v in audio_characteristics_totals_dict.items()}

    audio_characteristics_average_list = []
    for average in audio_characteristics_average_dict: 
        audio_characteristics_average = {
            'name': 'Positivity' if average == 'valence' else average.capitalize(),
            'average': round(audio_characteristics_average_dict.get(average) * 100),
        }
        audio_characteristics_average_list.append(audio_characteristics_average)

    return audio_characteristics_average_list

