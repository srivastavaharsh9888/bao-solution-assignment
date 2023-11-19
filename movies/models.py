from django.db import models

class Actor(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    eye_color = models.CharField(max_length=100, null=True, blank=True)
    hair_color = models.CharField(max_length=100, null=True, blank=True)
    species_url = models.URLField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    original_title_romanised = models.CharField(max_length=200, null=True, blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    movie_banner = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField()
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    release_date = models.CharField(max_length=4)
    running_time = models.CharField(max_length=50)
    rt_score = models.CharField(max_length=10, null=True, blank=True)
    url = models.URLField(max_length=500)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title
