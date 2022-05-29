from django.contrib import admin

# Register your models here.
from .models import ConvertorModelForEverything, Tracks , UserTracks
admin.site.register(Tracks)

admin.site.register(UserTracks)

admin.site.register(ConvertorModelForEverything)