from db.models import Movie
from typing import List
from django.db.models.query import QuerySet
from django.db import transaction


def get_movies(
        title: str = None,
        actors_ids: List[int] = None,
        genres_ids: List[int] = None
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()
    if title:
        queryset = queryset.filter(title__icontains=title)
    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)
    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)
    return queryset


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    actors_ids: List[int],
    genres_ids: List[int],
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )
    movie.actors.set(actors_ids)
    movie.genres.set(genres_ids)
    return movie
