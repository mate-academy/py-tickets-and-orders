from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None,
    title: str | None = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None,
) -> Movie:
    if genres_ids and not all(isinstance(i, int) for i in genres_ids):
        raise ValueError("Invalid genre id")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids:
        movie.genres.set(genres_ids)

    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
