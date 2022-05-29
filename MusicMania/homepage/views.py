
# from multiprocessing.connection import Listener
from django.shortcuts import render,redirect


from recommender.models import Tracks,UserTracks,ConvertorModelForEverything
from django.db.models import Q
from django.contrib import messages

from .extrafunctions import addimages,toformat
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required




@login_required
def home(request):
    #read top 40 songs and display on homepage ,named explore
    # the post request works on clicking add to playlist button .it adds the user,song,date to UserTracks model.


    somerows = Tracks.objects.all()[:20]

    trackstopass = read_frame(somerows)
    trackstopass = addimages(trackstopass)

    tracks = toformat(trackstopass)

    context = {
        'tracks': tracks
    }

    
    if request.method == 'POST':
        SongToAdd = request.POST.get('addsong')
        ListenerUser = request.user
        existrecord = UserTracks.objects.filter(Listener = ListenerUser,Song = SongToAdd)
        if(not existrecord):
            #prevent duplicates
            newentry = UserTracks(Listener_id = ListenerUser.id, Song_id = SongToAdd) # create new model instance
            newentry.save() #save to db
            messages.success(request,f'song added to your songs dear {ListenerUser.username}!')
            return redirect('homepage-listenedsongs')    
    
    return render(request,'homepage/home.html',context)





def about(request):
    return render(request,'homepage/about.html')


@login_required
def search(request):
    if request.method == "POST":
        # if search request then search by song name or artist name
        searchbar = request.POST.get('valuesearched')
        SongList = Tracks.objects.filter(Q(name__contains = searchbar) | Q(artists__contains = searchbar)  )
        trackstopass = read_frame(SongList)
        trackstopass = addimages(trackstopass)

        tracks = toformat(trackstopass)

        
        return render(request,'homepage/searchutil.html',{'searchbar':searchbar,'SongList':tracks})
    else:
        return render(request,'homepage/searchutil.html',{})

@login_required
def listenedsongs(request):
    #the post request gets triggered when we want to delete the song from our playlist

    if request.method == 'POST':
        SongToDel = request.POST.get('delsong')
        ListenerUser = request.user

        entrytodel = UserTracks.objects.filter(Listener_id = ListenerUser.id, Song_id = SongToDel) # find the model instance
        entrytodel.delete() #del to db
        messages.success(request,f'song deleted from your songs dear {ListenerUser.username}!')
        return redirect('homepage-listenedsongs')    


    #else just show the user's playlist
    ListenerUser = request.user
    SongList = UserTracks.objects.filter(Listener = ListenerUser)
    List=[]
    for row in SongList:
        List.append(row.Song)

    SongList = Tracks.objects.filter(id__in = List)
    trackstopass = read_frame(SongList)
    trackstopass = addimages(trackstopass)

    tracks = toformat(trackstopass)
    
    return render(request,'homepage/ListenedSongs.html',{'SongList':tracks})

# @login_required
# def recommended(request):
#     return render(request,'recommended/recommended.html',{})
