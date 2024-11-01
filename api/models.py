from django.db import models

# Create your models here.
class SpotifyToken(models.Model): 
    session_id = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=200)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    refresh_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
