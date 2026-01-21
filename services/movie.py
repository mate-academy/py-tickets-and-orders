from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


@transaction.atomic
def create_movie(movie_title: str, movie_description: str) -> Movie:
    return Movie.objects.create(title=movie_title, description=movie_description)


def get_movies(title: str = None) -> QuerySet:
    queryset = Movie.objects.all()
    if title:
        queryset = queryset.filter(title__icontains=title)
    return queryset
