from django.contrib import admin

from movies.models import Movie, Actor

admin.site.register(Movie)
admin.site.register(Actor)