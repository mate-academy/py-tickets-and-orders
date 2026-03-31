from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


from django.db.models import Q


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    filters = Q()

    if genres_ids:
        filters &= Q(genres__id__in=genres_ids)

    if actors_ids:
        filters &= Q(actors__id__in=actors_ids)

    if title:
        filters &= Q(title__icontains=title)

    return queryset.filter(filters)


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
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
