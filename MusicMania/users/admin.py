from django.contrib import admin

# Register your models here.
#register profile model to be visible on django admin page
from .models import Profile
admin.site.register(Profile)