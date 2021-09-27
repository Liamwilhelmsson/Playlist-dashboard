from django.urls import path
from .views import Login, Callback, IsAuthenticated, Logout, Playlists, PlaylistData

app_name = 'api'

urlpatterns = [
    path('login', Login.as_view()),
    path('logout', Logout.as_view()), 
    path('callback', Callback.as_view()),
    path('is-authenticated', IsAuthenticated().as_view()),
    path('playlists', Playlists().as_view()),
    path('playlist-data', PlaylistData().as_view())
]
