from django.db.models import QuerySet
from django.db import transaction
from typing import Optional

from db.models import Movie


def get_movies(
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
    title: Optional[str] = None
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[list] = None,
    actors_ids: Optional[list] = None,
) -> Movie | None:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )
        if genres_ids is not None:
            movie.genres.set(genres_ids)
        if actors_ids is not None:
            movie.actors.set(actors_ids)

        return movie
