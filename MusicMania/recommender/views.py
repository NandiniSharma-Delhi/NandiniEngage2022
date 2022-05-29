
from django.shortcuts import render
from multiprocessing.connection import Listener

from .models import ConvertorModelForEverything, Tracks,UserTracks
# from django.db.models import Q

# pandas is needed here to read the csv file and fill the database once
import pandas as pd

#  engine.py is the ----  RECOMMENDER ENGINE ---- model written as python file and imported as module to use its functions
from . import engine

from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required





"""
the following commented code is used to load Tracks table with data from tracksFinal.csv.
This code is uncommented once in the start and then run python manage.py makemigrations
then comment the code again as it is no longer needed
"""


# tracksfile=pd.read_csv('recommender/tracksFinal.csv',sep=',')
# tracksfile.drop_duplicates('id',inplace = True)

# tracks = [
#     Tracks(
#         id = row['id'],
#         name = row['name'],
#         popularity = row['popularity'],
#         duration_ms =row['duration_ms'],
#         explicit =row['explicit'],
#         artists = row['artists'],
#         id_artists = row['id_artists'],
#         release_date = row['release_date'],
#         danceability = row['danceability'],
#         energy = row['energy'],
#         key = row['key'],
#         loudness = row['loudness'],
#         mode = row['mode'],
#         speechiness = row['speechiness'],
#         acousticness = row['acousticness'],
#         instrumentalness = row['instrumentalness'],
#         liveness = row['liveness'],
#         valence = row['valence'],
#         tempo = row['tempo'],
#         time_signature = row['time_signature'],
#     )
#     for index,row in tracksfile.iterrows()
# ]
# Tracks.objects.bulk_create(tracks,ignore_conflicts=True)

complete_feature_set,spotify_df = engine.startworking()




@login_required
def djangoml(request):
    ListenerUser = request.user
    SongList = UserTracks.objects.filter(Listener = ListenerUser)
    List=[] # get list of ids of user's songs
    for row in SongList:
        List.append(row.Song)


    completeList = Tracks.objects.filter(id__in = List)
    SongList_df1= read_frame(completeList)
    SongList_df2 = read_frame(SongList)
    SongList_df1['Song']=SongList_df1['id']
    SongList_df3 = SongList_df1.merge(SongList_df2[['Song','date_added']], on = 'Song', how = 'inner')  # dataframe with date_added col added to all songdata
    

    if SongList_df3.size==0:
        tracks = {}  #when no song in playlist
    else :

        
        complete_feature_set_playlist_vector_EDM, complete_feature_set_nonplaylist_EDM = engine.generate_playlist_feature(complete_feature_set, SongList_df3, 1.09,spotify_df)
        songRecommended = engine.generate_playlist_recos(spotify_df, complete_feature_set_playlist_vector_EDM, complete_feature_set_nonplaylist_EDM)

        del complete_feature_set_nonplaylist_EDM
        del complete_feature_set_playlist_vector_EDM
        # del complete_feature_set,spotify_df

        songRecommended = engine.addimages(songRecommended)
        tracks = engine.toformat(songRecommended)

    return render(request,'homepage/recommended.html',{'SongList':tracks})

