
# movies/views.py
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing movies.
    """
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer

    # Cache the results of the `list` action for 1 minute (60 seconds)
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Optionally, cache the `retrieve` action as well
    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)