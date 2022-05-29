import pandas as pd

from recommender.models import ConvertorModelForEverything



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

import warnings
warnings.filterwarnings("ignore")


######################################



# function to add images and songurls to songs in playlist


def addimages(playlist):
    client_id = 'c1989b827388428091a3f497fee66fa7' #ignore
    client_secret= '31a8f83c6782438fba9c750ec50eb260'
    scope = 'user-library-read'
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret) #ignore
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # token = util.prompt_for_user_token(scope, client_id= client_id, client_secret=client_secret, redirect_uri='http://localhost:8881/') #ignore
    # sp = spotipy.Spotify(auth=token)

    
    playlist['url'] = playlist['id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
    playlist['playurl'] = playlist['id'].apply(lambda x: sp.track(x)['preview_url'])

    return playlist


# function to convert playlist into queryset like form
def toformat(playlist):
    playlist2 = [
        ConvertorModelForEverything(
        id = row['id'],
        name = row['name'],
        popularity = row['popularity'],
        duration_ms =row['duration_ms'],
        explicit =row['explicit'],
        artists = row['artists'],
        id_artists = row['id_artists'],
        release_date = row['release_date'],
        danceability = row['danceability'],
        energy = row['energy'],
        key = row['key'],
        loudness = row['loudness'],
        mode = row['mode'],
        speechiness = row['speechiness'],
        acousticness = row['acousticness'],
        instrumentalness = row['instrumentalness'],
        liveness = row['liveness'],
        valence = row['valence'],
        tempo = row['tempo'],
        time_signature = row['time_signature'],
        image_f1 = row['url'],
        songplay_f1 = row['playurl'],

    )
    for index,row in playlist.iterrows()
    ]

    return playlist2
