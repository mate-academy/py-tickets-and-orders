from __future__ import annotations

from typing import Optional

from django.db.models import QuerySet
from django.db.transaction import atomic

from db.models import Movie


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    elif genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    elif actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie | str:
    try:
        return Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return f"Movie with id {movie_id} doesn`t exist"


@atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[list] = None,
    actors_ids: Optional[list] = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
