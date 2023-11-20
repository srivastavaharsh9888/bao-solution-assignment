from django.test import TestCase
from ..models import Actor, Movie

class ActorModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        Actor.objects.create(
            id="a123",
            name="John Doe",
            gender="Male",
            age="30",
            eye_color="Blue",
            hair_color="Black",
            species_url="http://example.com/species",
            url="http://example.com/actor"
        )

    def test_actor_str(self):
        actor = Actor.objects.get(id="a123")
        self.assertEqual(str(actor), "John Doe")

class MovieModelTest(TestCase):
    def setUp(self):
        # Create an actor for the movie
        self.actor = Actor.objects.create(id="a123", name="John Doe")

        # Create a movie
        Movie.objects.create(
            id="m456",
            title="Sample Movie",
            original_title="Original Title",
            original_title_romanised="Original Title Romanised",
            image="http://example.com/image.jpg",
            movie_banner="http://example.com/banner.jpg",
            description="Sample movie description",
            director="Jane Smith",
            producer="Jim Bean",
            release_date="2021",
            running_time="120",
            rt_score="95",
            url="http://example.com/movie"
        )

    def test_movie_str(self):
        movie = Movie.objects.get(id="m456")
        self.assertEqual(str(movie), "Sample Movie")

    def test_movie_actors(self):
        movie = Movie.objects.get(id="m456")
        movie.actors.add(self.actor)
        self.assertIn(self.actor, movie.actors.all())
