from django.db import transaction
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from db.models import Movie


def get_movies(
    genres_ids: list[int] = [],
    actors_ids: list[int] = [],
    title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    try:
        return Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise ObjectDoesNotExist(f"Movie with id {movie_id} does not exist.")


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
) -> Movie:
    genres_ids = genres_ids or []  # Якщо genres_ids = None, встановлюємо порожній список
    actors_ids = actors_ids or []  # Якщо actors_ids = None, встановлюємо порожній список

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
