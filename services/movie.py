from django.db.models import QuerySet
from db.models import Movie
from django.db import transaction


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet:
    if title is not None:
        queryset = Movie.objects.all().filter(title__icontains=title)
    else:
        queryset = Movie.objects.all()

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
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    with transaction.atomic():
        film = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )
        if genres_ids:
            film.genres.set(genres_ids)
        if actors_ids:
            film.actors.set(actors_ids)

        return film
