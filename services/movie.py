from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
        genres_ids: list[int] = None,
        actors_ids: list[int] = None,
        title: str = None
) -> QuerySet:
    if title:
        movie = Movie.objects.filter(
            title__icontains=title).values_list("title")
    else:
        movie = Movie.objects.all()

    if genres_ids:
        movie = movie.filter(genres__id__in=genres_ids)

    if actors_ids:
        movie = movie.filter(actors__id__in=actors_ids)

    return movie


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
