import pandas as pd
import numpy as np
import json
import re
import sys
import itertools
from recommender.models import ConvertorModelForEverything
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# import spotipy to get song images and song urls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

import warnings

warnings.filterwarnings("ignore")


######################################### data procesing #############################


# first function to convert data in tracksFinal.csv to complete_feature_set and create dataframe spotify_df
def startworking():
    # read datafiles
    spotify_df = pd.read_csv('recommender/tracksFinal.csv')
    data_w_genre = pd.read_csv('recommender/artists.csv')

    data_w_genre['genres_upd'] = data_w_genre['genres'].apply(
        lambda x: [re.sub(' ', '_', i) for i in re.findall(r"'([^']*)'", x)])  # convert string genres to list of genres
    data_w_genre['artists'] = data_w_genre['name']  # change col name to col artists
    del data_w_genre['name']  # delete col name

    spotify_df['artists_upd_v1'] = spotify_df['artists'].apply(
        lambda x: re.findall(r"'([^']*)'", x))  # convert artists string to list as artists_upd_v1
    spotify_df['artists_upd_v2'] = spotify_df['artists'].apply(
        lambda x: re.findall('\"(.*?)\"', x))  # artist names with apostrophe
    spotify_df['artists_upd'] = spotify_df['artists_upd_v1'] + spotify_df['artists_upd_v2']  # add both lists
    spotify_df['artists_song'] = spotify_df.apply(lambda row: str(row['artists_upd'][0]) + str(row['name']),
                                                  axis=1)  # create a new col with concatenated names of artists and song
    spotify_df.sort_values(['artists_song', 'release_date'], ascending=False, inplace=True)  # sort
    spotify_df.drop_duplicates('artists_song', inplace=True)  # drop duplicates

    # add genre data to song data
    artists_exploded = spotify_df[['artists_upd', 'id']].explode('artists_upd')
    artists_exploded_enriched = artists_exploded.merge(data_w_genre, how='left', left_on='artists_upd',
                                                       right_on='artists')
    artists_exploded_enriched_nonnull = artists_exploded_enriched[~artists_exploded_enriched.genres_upd.isnull()]
    artists_exploded_enriched_nonnull['id'] = artists_exploded_enriched_nonnull['id_x']
    del artists_exploded_enriched_nonnull['id_x']  # del unwanted col

    # consolidated genre list
    artists_genres_consolidated = artists_exploded_enriched_nonnull.groupby('id')['genres_upd'].apply(
        list).reset_index()
    artists_genres_consolidated['consolidates_genre_lists'] = artists_genres_consolidated['genres_upd'].apply(
        lambda x: list(set(list(itertools.chain.from_iterable(x)))))

    # finally merge genrelist with songdata
    spotify_df = spotify_df.merge(artists_genres_consolidated[['id', 'consolidates_genre_lists']], on='id', how='left')

    # add year col
    spotify_df['year'] = spotify_df['release_date'].apply(lambda x: x.split('-')[0])

    # columns with float datatype
    float_cols = spotify_df.dtypes[spotify_df.dtypes == 'float64'].index.values

    # divide popularity by 5 to create popularity buckets
    spotify_df['popularity_red'] = spotify_df['popularity'].apply(lambda x: int(x / 5))
    spotify_df['consolidates_genre_lists'] = spotify_df['consolidates_genre_lists'].apply(
        lambda d: d if isinstance(d, list) else [])

    # create featureset having  genre and year data
    # initially we used the following commented line to create feauture sets for all songs but then we can directly save that processed data in completeFeatures.csv to save us the time of executing functions:ohe_prep and create_feature_set
    # these functions have not been deleted so that you can uderstand how this "complleteFeatures.csv" has been created
    # complete_feature_set = create_feature_set(spotify_df, float_cols=float_cols)
    complete_feature_set = pd.read_csv('recommender/completeFeatures.csv')

    return complete_feature_set, spotify_df


########################################data changing finnished ################

def ohe_forcols(df, column, new_name):
    """
    creates one hot encoding of given column and saves as a renamed col
    """

    colum = pd.get_dummies(df[column])
    feature_names = colum.columns
    colum.columns = [new_name + "|" + str(i) for i in feature_names]
    colum.reset_index(drop=True, inplace=True)
    return colum


###############################################
def create_feature_set(df, float_cols):
    """
    Process spotify df to create a final set of features that will be used to generate recommendations.
    give the list of cols to be scaled.

    """

    # tfidf genre lists
    tfidfgenre = TfidfVectorizer()
    tfidf_matrix = tfidfgenre.fit_transform(df['consolidates_genre_lists'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidfgenre.get_feature_names()]
    genre_df.reset_index(drop=True, inplace=True)

    # one hot encoding of year and popularity
    year_ohe = ohe_forcols(df, 'year', 'year') * 0.5
    popularity_ohe = ohe_forcols(df, 'popularity_red', 'pop') * 0.15

    # scale float columns
    floats = df[float_cols].reset_index(drop=True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns=floats.columns) * 0.2

    # concanenate all features
    feature_set = pd.concat([genre_df, floats_scaled, popularity_ohe, year_ohe], axis=1)

    # add song id
    feature_set['id'] = df['id'].values

    return feature_set


########################### works on input playlist #################################################

def generate_playlist_feature(completeFeatures, playlistofuser_df, weight_factor, df):
    """
    Summarize a user's playlist into a single vector.

    more is weight factor,more importance recency gets.

    playlist_feature_set_weighted_final : single feature that summarizes the playlist
    """

    # retain songs which are already in database.sort descending according to date added so that we can extract most recent song
    playlistofuser_df = playlistofuser_df[playlistofuser_df['id'].isin(df['id'].values)].sort_values('date_added',
                                                                                                     ascending=False)

    # convert date_added col to datetime type
    playlistofuser_df['date_added'] = pd.to_datetime(playlistofuser_df['date_added'])

    # features of playlist songs
    complete_feature_set_playlist = completeFeatures[
        completeFeatures['id'].isin(playlistofuser_df['id'].values)]  # .drop('id', axis = 1).mean(axis =0)

    # add date_added col
    complete_feature_set_playlist = complete_feature_set_playlist.merge(playlistofuser_df[['id', 'date_added']],
                                                                        on='id', how='inner')

    # features of nonplaylist songs
    complete_feature_set_nonplaylist = completeFeatures[
        ~completeFeatures['id'].isin(playlistofuser_df['id'].values)]  # .drop('id', axis = 1)

    # sort on date_added descending
    playlist_feature_set = complete_feature_set_playlist.sort_values('date_added', ascending=False)

    # most recent date
    most_recent_date = playlist_feature_set.iloc[0, -1]

    # add a months_from_recent date column
    for ix, row in playlist_feature_set.iterrows():
        playlist_feature_set.loc[ix, 'months_from_recent'] = int(
            (most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days / 30)

    playlist_feature_set['weight'] = playlist_feature_set['months_from_recent'].apply(lambda x: weight_factor ** (-x))

    # playlist_feature_set_weighted = playlist_feature_set.copy()

    # playlist_feature_set_weighted.update(playlist_feature_set_weighted.iloc[:,:-4].mul(playlist_feature_set_weighted.weight,0))
    # playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-4]

    playlist_feature_set.update(playlist_feature_set.iloc[:, :-4].mul(playlist_feature_set.weight, 0))
    playlist_feature_set_weighted_final = playlist_feature_set.iloc[:, :-4]

    return playlist_feature_set_weighted_final.sum(axis=0), complete_feature_set_nonplaylist


def generate_playlist_recos(dataf, playlist_features, nonplaylist_features):
    """
        apply cosine similarity and sort to get top 20 recommendations
    """

    non_playlist_df = dataf[dataf['id'].isin(nonplaylist_features['id'].values)]
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis=1).values,
                                               playlist_features.values.reshape(1, -1))[:, 0]
    top20tracks = non_playlist_df.sort_values('sim', ascending=False).head(20)

    return top20tracks


#####################################to get images url from spotify#########################


def addimages(playlist):
    """
    add song images and songurls from spotipy using songids
    """

    # hardcoded client_id
    # currently I am using my id otherwise you can
    client_id = 'c1989b827388428091a3f497fee66fa7'
    client_secret = '31a8f83c6782438fba9c750ec50eb260'
    # scope = 'user-library-read'
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)  # ignore
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # token = util.prompt_for_user_token(scope, client_id= client_id, client_secret=client_secret, redirect_uri='http://localhost:8881/') #ignore
    # sp = spotipy.Spotify(auth=token)

    # add url=imageurl  playurl=url to play song 30sec sample
    playlist['url'] = playlist['id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
    playlist['playurl'] = playlist['id'].apply(lambda x: sp.track(x)['preview_url'])

    return playlist


def toformat(playlist):
    playlist2 = [
        ConvertorModelForEverything(
            id=row['id'],
            name=row['name'],
            popularity=row['popularity'],
            duration_ms=row['duration_ms'],
            explicit=row['explicit'],
            artists=row['artists'],
            id_artists=row['id_artists'],
            release_date=row['release_date'],
            danceability=row['danceability'],
            energy=row['energy'],
            key=row['key'],
            loudness=row['loudness'],
            mode=row['mode'],
            speechiness=row['speechiness'],
            acousticness=row['acousticness'],
            instrumentalness=row['instrumentalness'],
            liveness=row['liveness'],
            valence=row['valence'],
            tempo=row['tempo'],
            time_signature=row['time_signature'],
            image_f1=row['url'],
            songplay_f1=row['playurl'],

        )
        for index, row in playlist.iterrows()
    ]

    return playlist2


