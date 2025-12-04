from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
    title: Optional[str] = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)
        queryset = queryset.order_by("id")

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list,
    actors_ids: list,
) -> Movie:
    if any(not isinstance(i, int) for i in genres_ids):
        raise ValueError("All genre IDs must be integers")

    if any(not isinstance(i, int) for i in actors_ids):
        raise ValueError("All actor IDs must be integers")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    movie.genres.set(genres_ids)
    movie.actors.set(actors_ids)

    return movie
