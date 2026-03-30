from typing import Optional, List
from django.db.models import QuerySet
from django.db import transaction

from db.models import Movie


def get_movies(title: Optional[str] = None) -> QuerySet[Movie]:
    movies = Movie.objects.all()
    if title:
        movies = movies.filter(title__icontains=title)
    return movies


@transaction.atomic
def create_movie(
    title: str,
    description: str,
    genres: List[int],
    actors: List[int]
) -> Movie:
    movie = Movie.objects.create(
        title=title,
        description=description
    )
    movie.genres.set(genres)
    movie.actors.set(actors)
    return movie
