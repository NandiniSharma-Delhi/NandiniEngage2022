from django.db import models
# from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.




class Tracks(models.Model):
    id = models.CharField(max_length = 1000,primary_key = True)
    name = models.CharField(max_length = 1000)
    popularity = models.BigIntegerField()
    duration_ms =models.BigIntegerField()
    explicit =models.BigIntegerField()
    artists = models.CharField(max_length = 1000)
    id_artists = models.CharField(max_length = 1000)
    release_date = models.CharField(max_length = 1000)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.BigIntegerField()
    loudness = models.FloatField()
    mode = models.BigIntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.BigIntegerField()


    def __str__(self):
        return self.id



class UserTracks(models.Model):
    Listener = models.ForeignKey(User, on_delete=models.CASCADE )
    Song = models.ForeignKey(Tracks, on_delete=models.CASCADE )
    date_added = models.DateTimeField(default = timezone.now)




class ConvertorModelForEverything(models.Model):
    id = models.CharField(max_length = 1000,primary_key = True)
    name = models.CharField(max_length = 1000)
    popularity = models.BigIntegerField()
    duration_ms =models.BigIntegerField()
    explicit =models.BigIntegerField()
    artists = models.CharField(max_length = 1000)
    id_artists = models.CharField(max_length = 1000)
    release_date = models.CharField(max_length = 1000)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.BigIntegerField()
    loudness = models.FloatField()
    mode = models.BigIntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.BigIntegerField()
    date_added = models.DateTimeField(default = timezone.now)
    image_f1 = models.URLField()
    image_f2 = models.URLField()
    songplay_f1 = models.URLField()
    songplay_f1 = models.URLField()




    def __str__(self):
        return self.id

