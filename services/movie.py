from typing import Optional

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Movie


def get_movies(
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
    title: Optional[str] = None
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__contains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return get_object_or_404(Movie, id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> None:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)
