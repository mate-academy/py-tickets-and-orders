from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional

from db.models import Movie


def get_movies(
        genres_ids: Optional[list[int]] = None,
        actors_ids: Optional[list[int]] = None,
        title: Optional[str] = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    queryset = queryset.order_by("title")

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    try:
        return Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise ValidationError(f"Movie with id {movie_id} does not exist")


def create_movie(
        movie_title: str,
        movie_description: str,
        genres_ids: Optional[list] = None,
        actors_ids: Optional[list] = None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )
        if genres_ids:
            movie.genres.set(genres_ids)
        if actors_ids:
            movie.actors.set(actors_ids)

    return movie
