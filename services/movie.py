from django.db import transaction
from django.db.models import QuerySet, Q

from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None
) -> QuerySet:
    queryset = Q()

    if genres_ids:
        queryset.add(Q(genres__id__in=genres_ids), Q.AND)

    if actors_ids:
        queryset.add(Q(actors__id__in=actors_ids), Q.AND)

    if title:
        queryset.add(Q(title__icontains=title), Q.AND)

    return Movie.objects.filter(queryset)


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
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
