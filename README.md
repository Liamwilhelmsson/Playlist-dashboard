# Playlist-dashboard

This application uses Spotify Web API to display information of your playlists from Spotify.
The application uses React.js as frontend and Django with Django REST framework as well as PostgreSQL on the backend.

![Playlist_dashboard](https://user-images.githubusercontent.com/21284111/135754688-d7103601-61f5-434a-ae13-1e380f26175f.PNG)

## Spotify API

Application uses the following endpoints:

- [Authorization](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)
- [Get a List of a User's Playlists](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-list-users-playlists)
- [Get a Playlist's Items](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-playlists-tracks)
- [Get Artists](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-multiple-artists)
- [Get Audio Features](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-several-audio-features)

## Setup

### Install Python Modules

```bash
pip install -r requirements.txt
```

### Install Node modules

[Install Node.js](https://nodejs.org/en/)

Navigate to frontend folder and run:

```bash
npm install
```

### Secret key

```bash
$ python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add secret key to secrets.json

### Connect database

[Install PostgreSQL](https://www.postgresql.org/)

Add database _Name_ , _User_ , _Password_ , _Host_ and _Port_ to secrets.json

Run:

```bash
manage.py migrate
```

### Create Spotify App

Login and create a new app on https://developer.spotify.com/dashboard/.

Add `http://127.0.0.1:8000/api/callback` as _Redirect URI_ in your Spotify App Settings.

Add _Client Id_ and _Client Secret_ to secrets.json.

## Run app

### Run backend

```bash
manage.py runserver
```

### Compile frontend

```bash
npm run build
```
