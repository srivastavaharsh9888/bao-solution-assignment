import time
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Movie
from django.core.cache import cache
from django.utils.cache import get_cache_key
from urllib.parse import quote as urlquote

class MovieViewSetTest(APITestCase):


    def setUp(self):
        # Set up data for the whole TestCase
        self.movie1 = Movie.objects.create(
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

        self.movie2 =  Movie.objects.create(
            id="m4561",
            title="Sample Movie 2",
            original_title="Original Title 2",
            original_title_romanised="Original Title Romanised 2",
            image="http://example.com/image2.jpg",
            movie_banner="http://example.com/banner2.jpg",
            description="Sample movie for second one",
            director="Jane Smith second diretor",
            producer="Jim Bean seconf producer",
            release_date="2023",
            running_time="240",
            rt_score="97",
            url="http://example2.com/movie"
        )

        self.list_url = reverse('movie-list')
        self.detail_url = reverse('movie-detail', args=[self.movie1.id])

    def test_list_movies(self):
        # Mocking the authentication for simplicity
        self.client.credentials(HTTP_GHIBLIKEY='QAZWSXEDCRFVTGBYHNUJMIKOL!)(@*#&$^%)')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)
        # Assuming the movies are ordered by release_date in descending order
        self.assertGreaterEqual(response.data[0]['release_date'], response.data[1]['release_date'])

    def test_retrieve_movie(self):
        # Mocking the authentication
        self.client.credentials(HTTP_GHIBLIKEY='QAZWSXEDCRFVTGBYHNUJMIKOL!)(@*#&$^%)')

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.movie1.id)

    def test_authentication_required(self):
        # Test without providing API key
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_movie_list_caching(self):
        self.client.credentials(HTTP_GHIBLIKEY='QAZWSXEDCRFVTGBYHNUJMIKOL!)(@*#&$^%)')

        response1 = self.client.get(self.list_url)
        first_content = response1.content

        # Wait for a short time (less than cache duration)
        time.sleep(1)  # Adjust the sleep time as needed


        # Make the second request
        response2 = self.client.get(self.list_url)
        second_content = response2.content

        # Compare the responses; they should be the same if caching works
        self.assertEqual(first_content, second_content)

        # Make a change that should affect the response
        Movie.objects.create(id="m4563",
            title="Sample Movie 2",
            original_title="Original Title 2",
            original_title_romanised="Original Title Romanised 2",
            image="http://example.com/image2.jpg",
            movie_banner="http://example.com/banner2.jpg",
            description="Sample movie for second one",
            director="Jane Smith second diretor",
            producer="Jim Bean seconf producer",
            release_date="2023",
            running_time="240",
            rt_score="97",
            url="http://example2.com/movie")  # Create a new movie

        time.sleep(62)  # Adjust the sleep time as needed
        response2 = self.client.get(self.list_url)
        second_content = response2.content
        self.assertNotEqual(first_content, second_content)
