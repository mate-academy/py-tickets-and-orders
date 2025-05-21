from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie, Genre, Actor


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title is not None:
        queryset = queryset.filter(title__icontains=title)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )
        if genres_ids:
            existing_genres = Genre.objects.filter(id__in=genres_ids)
            if existing_genres.count() != len(genres_ids):
                missing_genres_ids = (
                    set(genres_ids)
                    - set(existing_genres.values_list("id", flat=True)))
                raise ObjectDoesNotExist(
                    f"One or more genres with IDs {list(missing_genres_ids)} "
                    "do not exist."
                )
            movie.genres.set(existing_genres)
        if actors_ids:
            existing_actors = Actor.objects.filter(id__in=actors_ids)
            if existing_actors.count() != len(actors_ids):
                missing_actors_ids = (
                    set(actors_ids)
                    - set(existing_actors.values_list("id", flat=True)))
                raise ObjectDoesNotExist(
                    f"One or more actors with IDs {list(missing_actors_ids)} "
                    "do not exist."
                )
            movie.actors.set(existing_actors)

    return movie
