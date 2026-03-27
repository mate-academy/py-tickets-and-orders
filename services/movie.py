from django.db.models import QuerySet
from django.db import transaction

from db.models import Movie


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(title, description):
    movie = Movie.objects.create(title=title, description=description)
    return movie

def get_movies(title=None):
    if title:
        return Movie.objects.filter(title__icontains=title)
    return Movie.objects.all()
