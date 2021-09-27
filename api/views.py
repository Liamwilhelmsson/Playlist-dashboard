from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_100_CONTINUE, HTTP_200_OK
from rest_framework.views import APIView
from .auth_services import *
from .spotify_services import *

class Login(APIView): 
    '''
    Returns the url for the spotify authentication
    '''
    def get(self, request, format=None):
        auth_url = get_auth_url()
        return Response({'url': auth_url}, status=status.HTTP_200_OK)


class Callback(APIView): 
    '''
    Process callback from spotify.
    Request access token and create a new Spotify token before redirecting back to frontend
    '''
    def get(self, request, format=None):
        code = request.GET.get('code')

        # Request acess token with authorization code
        response = request_access_token(code) 
        access_token = response['access_token']
        token_type = response['token_type']
        expires_in = response['expires_in']
        refresh_token = response['refresh_token']

        # Create new session if there isn't one in the request 
        if not request.session.exists(request.session.session_key):
            request.session.create()

        create_or_refresh_access_token(request.session.session_key, access_token,
                                    token_type, expires_in, refresh_token)

        return redirect('frontend:')



class Logout(APIView): 
    '''  Logout the current session by deleting the connected spotifyToken from the database  '''

    def post(self, request, format=None):
        if request.session.exists(request.session.session_key):
            delete_spotify_token(request.session.session_key)
            return Response({'Message': 'User logout sucessful'}, status=status.HTTP_200_OK)       
        else:
            return Response({'Message': 'User not logged in'}, status=status.HTTP_200_OK) 


class IsAuthenticated(APIView): 
    ''' Check if the current session is authenticated '''

    # Gets the url for the spotify authentication
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)

        return Response({'is_authenticated': is_authenticated}, status=status.HTTP_200_OK)


# Gets list of playlists 
class Playlists(APIView): 
    ''' Returns a list of playlists: 
    {
        id: Spotify identifier for the playlist
        name: Name of playlist
        icon: Playlist icon url 
    } 
    '''

    def get(self, request, format=None):

        offset = 0
        playlists = []
        while True: 
            response = execute_spotify_api_request(self.request.session.session_key, f"/me/playlists?limit=50&offset={offset}", "GET")
            print(response)
            if 'error' in response:
                return Response(response, status=response['error']['status'])
            elif 'items' not in response:
                return Response({'error': 'No content'}, status=status.HTTP_204_NO_CONTENT)

            playlists = playlists + get_spotify_playlists(response)

            if len(response['items']) < 50:
                break 
            
            offset = offset + 50

        return Response({'playlists': playlists}, status=status.HTTP_200_OK)


# Gets information of playlist 
class PlaylistData(APIView): 
    ''' 
    Takes parameter: playlist_id
    
    Returns the following data for a given playlist: 
    {
        artistCount: { 
            name: Artist name
            tracks: Number of tracks they appeared on 
        }

        tracks: {
            id: Playlist id
            trackName: Name of the track
            artistName: Comma seperated string of the artists
            albumName: Album name
            albumCover: url to album cover 
        }

        genres: {
            name: Genre name
            tracks: Number of tracks that has that genre 
        }

        tracksPerDecade: {
            name: The decade
            average: The number of tracks in that decade
        }

        tracksPerBpm: {
            name: A bpm 
            tracks: Number of tracks with a bpm between the span
        }

        audioCharactersticsAverage: 
        {
            name: Audio characteristic ('danceability', 'energy', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'positivity')
            average: The average of the given characteristic (0-100)
        }
    '''

    def get(self, request, format=None):
        # Get playlist id from url 
        playlist_id = request.GET.get('playlist_id')

        tracks = get_tracks(self.request.session.session_key, playlist_id)   

        if 'error' in tracks:
            return Response({'playlistData': {}, 'error': tracks['error']}, status=tracks['status'])

        artist_count = get_artist_count(tracks)
        track_info = get_track_info(tracks)
        genres_count = get_genre_count(self.request.session.session_key, tracks)
        tracks_per_decade = get_tracks_per_decade(tracks)
        audio_features = get_audio_features(self.request.session.session_key, tracks)
        track_count_per_bpm = get_bpm_count(audio_features)
        audio_characteristics = get_audio_characteristics_average(audio_features)
     
        data = {
            'artistCount': artist_count,
            'tracks': track_info,
            'genresCount': genres_count,
            'tracksPerDecade': tracks_per_decade,
            'tracksPerBpm': track_count_per_bpm,
            'audioCharactersticsAverage': audio_characteristics,
        }
        return Response({'playlistData': data}, status=status.HTTP_200_OK)

