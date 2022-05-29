#link is 'homepage-ML'
from django.urls import path
from . import views


urlpatterns = [
    path('ml/', views.djangoml,name = 'homepage-ML'),
]