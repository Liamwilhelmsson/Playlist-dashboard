from requests.sessions import session
from requests import Request
from spotify_playlist_dashboard.settings import get_secret
from requests import post
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta


# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://127.0.0.1:8000/api/callback'
SCOPES = 'playlist-read-private'

def get_auth_url(): 
    ''' Prepares the url for the spotify authentication'''

    url = Request('GET', AUTH_URL, params={
        'scope': SCOPES,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': get_secret('CLIENT_ID')
    }).prepare().url

    return url

def request_access_token(code):
    ''' Request access token from spotify '''

    response = post(TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': get_secret('CLIENT_ID'),
        'client_secret': get_secret('CLIENT_SECRET')
    }).json()

    return response


def create_or_refresh_access_token(session_id, access_token, token_type, expires_in, refresh_token): 
    ''' Creates a new SpotifyToken or updates the already existing one '''

    token = get_token_or_none(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if token:
        # Update existsing row
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        # Create new row 
        token = SpotifyToken(session_id=session_id, access_token=access_token, 
                            refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)

        token.save()

def is_spotify_authenticated(session_id): 
    ''' Check if authenticated and refresh token if needed '''
    token = get_token_or_none(session_id)

    if token:
        # Refresh if token if expired
        if token.expires_in <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    ''' Get a new access token with refresh token '''
    refresh_token = get_token_or_none(session_id).refresh_token

    response = post(TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': get_secret('CLIENT_ID'),
        'client_secret': get_secret('CLIENT_SECRET'),
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type') 
    expires_in = response.get('expires_in')

    create_or_refresh_access_token(session_id, access_token, token_type, expires_in, refresh_token)


def delete_spotify_token(session_id):
    '''  Deletes a spotify token from given session id  '''

    token = get_token_or_none(session_id)

    if token: 
        token.delete()

def get_token_or_none(session_id):
    '''  Returns SpotifyToken for the session if exists  '''

    try: 
        return SpotifyToken.objects.get(session_id=session_id)
    except SpotifyToken.DoesNotExist: 
        return None