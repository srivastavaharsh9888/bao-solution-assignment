import requests
from celery import shared_task
from django.conf import settings
from .models import Movie, Actor
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

@shared_task
def fetch_movies_from_ghibli():
    movies_url = f"{settings.GHIBLI_API_BASE_URL}{settings.GHIBLI_API_MOVIES_ENDPOINT}"
    movies_response = requests.get(movies_url)
    if movies_response.status_code != 200:
        print("Something went wrong when fetching movies")
        return

    movies_data = movies_response.json()
    actor_urls = set()

    for movie_data in movies_data:
        for actor_url in movie_data['people']:
            if actor_url:
                actor_urls.add(actor_url)

    existing_actor_ids = set(Actor.objects.filter(
        id__in=[url.split('=')[-1] for url in actor_urls]
    ).values_list('id', flat=True))

    new_actors = []

    for actor_url in actor_urls:
        actor_id = actor_url.split('=')[-1]
        if actor_id not in existing_actor_ids:
            actor_response = requests.get(actor_url)
            if actor_response.status_code == 200:
                actor_data_list = actor_response.json()
                for actor_data in actor_data_list:
                    if actor_data['id'] not in existing_actor_ids:
                        new_actor = Actor(
                            id=actor_data['id'],
                            name=actor_data['name'],
                            gender=actor_data.get('gender'),
                            age=actor_data.get('age'),
                            eye_color=actor_data.get('eye_color'),
                            hair_color=actor_data.get('hair_color'),
                            species_url=actor_data.get('species'),
                            url=actor_data['url'],
                        )
                        new_actors.append(new_actor)
                        existing_actor_ids.add(actor_data['id'])

    Actor.objects.bulk_create(new_actors)

    for movie_data in movies_data:
        movie, created = Movie.objects.update_or_create(
            id=movie_data['id'],
            defaults={
                'title': movie_data['title'],
                'original_title': movie_data['original_title'],
                'original_title_romanised': movie_data.get('original_title_romanised'),
                'image': movie_data.get('image'),
                'movie_banner': movie_data.get('movie_banner'),
                'description': movie_data['description'],
                'director': movie_data['director'],
                'producer': movie_data['producer'],
                'release_date': movie_data['release_date'],
                'running_time': movie_data['running_time'],
                'rt_score': movie_data.get('rt_score'),
                'url': movie_data['url'],
            }
        )

        actor_ids = [url.split('=')[-1] for url in movie_data['people'] if url]
        actors = Actor.objects.filter(id__in=actor_ids)
        movie.actors.set(actors)
    cache.clear()
    print("Movies and actors data fetched from Ghibli API")

    
@shared_task
def fetch_people_from_ghibli():
    people_url = f"{settings.GHIBLI_API_BASE_URL}{settings.GHIBLI_API_PEOPLE_ENDPOINT}"
    people_response = requests.get(people_url)
    if people_response.status_code != 200:
        print("Something went wrong")
        return

    actors_data = people_response.json()
    actors_to_update_or_create = []

    for actor_data in actors_data:
        actor, _ = Actor.objects.get_or_create(
            id=actor_data['id'],
            defaults={
                'name': actor_data['name'],
                'gender': actor_data.get('gender'),
                'age': actor_data.get('age'),
                'eye_color': actor_data.get('eye_color'),
                'hair_color': actor_data.get('hair_color'),
                'species_url': actor_data.get('species'),
                'url': actor_data['url']
            }
        )
        if not actor._state.adding:
            actors_to_update_or_create.append(actor)

    Actor.objects.bulk_update(actors_to_update_or_create, ['name', 'gender', 'age', 'eye_color', 'hair_color', 'species_url', 'url'])       
    cache.clear() 
    print("Actors Data updates")