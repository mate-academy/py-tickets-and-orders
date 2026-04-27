from typing import List, Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
    title: Optional[str] = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids is not None:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids is not None:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: List[int],
    actors_ids: List[int],
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    movie.genres.set(genres_ids)
    movie.actors.set(actors_ids)

    return movie
