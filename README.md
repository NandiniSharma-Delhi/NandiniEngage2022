# NandiniEngage2022

Hi this is Music Mania Project.
By:Nandini Sharma
Os used:windows
web technologies : django , bootstrap5

It is a music recommender website.Currently not hosted.
It recommends music based on similarity of songs in terms of song audio features:tempo,danceability,etc.
and also based on popularity and year of songs in your playlist.

As I have done something in ml for the first time,please ignore my errors.:)

Reference for recommendation system code : https://github.com/madhavthaker/spotify-recommendation-system

###First of all follow the following steps to be able to run this website:


1.##create a folder named MusicManiaProject;
go to cmd(for windows) or similar terminals for linux.
change path to this folder.


2. ##creating a virtual environment:

inside this folder
install virtualenv(if not done already):   
$pip install virtualenv



create a virtual environment:
$virtualenv venvmusic

activate venvmuisc:
$venvmusic/Scripts/activate

Now with activated virtualenvironment venvmusic,continue the rest of the instructions

4.##install all necessary packages inside virtual environment:



$pip install django django-crispy-forms
$pip install pandas sklearn
$pip install django-pandas
$pip install spotipy
#other packages that may be required

$pip install csvImporter
$pip install python
$pip install itertools sys re json numpy


5.##get your django's secret key by making a sample django project:
$django-admin startproject testproject

6:##go to testproject/testproject/settings.py and copy your SECRET_KEY from there

7:##copy above given folder "MusicMania" inside your "MusicManiaProject" Folder 
so your MusicManiaProject folder now has 3 folders MusicMania and venvmusic and testproject

MusicManiaProject
|---MusicMania
|---testproject
|---venvmusic

8:##due to lack of space in gitrepo I have provided some files as drive links please download these files:

db.sqlite3:  https://drive.google.com/file/d/19mo2tQSeekKdDQMOGUHAxeqfAITPO2f9/view?usp=sharing
artists.csv:https://drive.google.com/file/d/1H8jRz7q6b1tWTlwrbdPNIQrCNDJX4vXM/view?usp=sharing
tracksFinal.csv:https://drive.google.com/file/d/1ldkqY9INz6qRxFUoIlK2BEikwGEjKaYY/view?usp=sharing
completeFeatures.csv:https://drive.google.com/file/d/1FWocx3-ieh8rBb8Lu0ogNR9DvQJAiZ9j/view?usp=sharing


9:## go to MusicManiaProject/MusicMania/recommender:
and copy files artists.csv,tracksFinal.csv,completeFeatures.csv in this folder

10:##go to MusicManiaProject/MusicMania
copy db.sqlite file there.


11:##go to MusicManiaProject/MusicMania/MusicMania/settings.py and scroll down to find SECRET_KEY.Replace this secretkey with your secretkey obtained in step 6.

9:##now with venvmusic activated, on terminal change directory to MusicManiaProject/MusicMania

10:run following commands:
$python manage.py makemigrations
$python manage.py migrate


11:##if spotify asks for login:
login to your account but first create a spotify developer account on:
on spotify developer website login.
then click on create app.
and create a app.
for that app copy your clientid and clientsecret
and open engine.py and extrafunctions.py 
replace the clientid and clientsecret written there with your ones.

if spotify does not ask for login,its fine.


12:
$python manage.py runserver

13:go to "http://localhost:8000"


14:you can login(register) and see the website working

###Website :

after login, website has pages: profile,logout,home,explore,recommended,My playlist,search

##profile:shows current user
##logout:to logout
##home:shows website name and about it.
##explore: shows trending songs based on data saved in tracksFinal.csv
##recommended: shows songs recommended based on songs saved in My playlist
if there is no song in My Playlist then it shows nothing.

##My playlist: contains songs I added to my playlist by clicking on add to playlist buttons on explore,recommended,searched songs
##search:can search songs based on song name and artist name only.

##music player:plays a welcome music already.if you want to play other song.Pause this player.sometimes you need to wait a few seconds after pausing.Then click on play button of the song you wish to play.it will show audio controls and image of that song.


###Time taken to load:
The laptop I used to test this website is a normal i7 machine.Not having huge disk space.

I will mention the website load time I observed on my machine:

running:

$python manage.py makemigrations
$python manage.py migrate
$python manage.py runserver

these commands can take a few minutes.Since data reading and loading needs to be done.

login to website can take 4-5 seconds

explore page can take 4-5 seconds at max
my playlist page can take 4-5 seconds at max

recommender page can take 18-25 seconds to load

search can take time based on the number of results in output of search.


### About recommendation engine:

1:It is a content based recommendation system

2:it uses spotipy to get images and song30sec demo urls

3:the engine.py file in recommender folder is the file doing it.

4:we used cosine similarity of various features such as genre,year,artists,danceability,etc.. to generate recommendations based on user's playlist.

###datasets:

dataset reference:https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-600k-tracks
tracksFinal.csv :contains a part of this big dataset.
artists.csv:contains data about artists and genre
completeFeatures.csv: obtained by running some functions on initial dataset.The functions used to obtain this dataset are written in engine.py.but the line is commented.So we directly read thsi file
instead of running those functions again to obtain this data.This is done for speedup in running website.


##engine.py:
content based recommendations.

it combines data from tracksFinal.csv and artists.csv  and does one hot encoding of year and popularity,tfidf on genre,scaling of float columns to make completeFeatures.csv.
then  take the user's playlist and extract featuresets for songs in playlist and for songs not in playlist.
Add date_added col to features_of_playlist and multipy weight to the number of months the other songs are older than most recent song.

calculate cosine similarity of all songs not in playlist.
and sort according to this score.
return top 20 songs .




