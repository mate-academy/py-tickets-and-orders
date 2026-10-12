from django.db import transaction
from typing import Optional
from django.db.models import QuerySet
from db.models import Actor, Genre, Movie


def get_movies(
    genres_ids : Optional[list[int]] = None,
    actors_ids : Optional[list[int]] = None,
    title : Optional[list[int]] = None,
) -> QuerySet[Movie]:
    movies = Movie.objects.all()

    if genres_ids is not None:
        movies = movies.filter(genres__id__in=genres_ids)

    if actors_ids is not None:
        movies = movies.filter(actors__id__in=actors_ids)

    if title is not None:
        movies = movies.filter(title__icontains=title)

    return movies.distinct().order_by("id")


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids is not None:
        movie.genres.set(
            Genre.objects.filter(id__in=genres_ids)
        )

    if actors_ids is not None:
        movie.actors.set(
            Actor.objects.filter(id__in=actors_ids)
        )

    return movie
