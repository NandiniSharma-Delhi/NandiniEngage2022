from django.urls import path
from . import views


urlpatterns = [
    path('', views.about,name = 'homepage-about'),
    path('home/', views.home,name = 'homepage-home'),
    path('searchresults/', views.search,name = 'homepage-search'),
    path('mySongs/', views.listenedsongs,name = 'homepage-listenedsongs'),
]