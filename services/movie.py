from typing import Optional, Iterable
from django.db import transaction
from db.models import Movie, Genre, Actor
from django.db.models import QuerySet


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[Iterable[int]] = None,
    actors_ids: Optional[Iterable[int]] = None
) -> QuerySet[Movie]:
    qs = Movie.objects.all().order_by("id")
    if title:
        qs = qs.filter(title__icontains=title)
    if genres_ids:
        qs = qs.filter(genres__id__in=genres_ids)
    if actors_ids:
        qs = qs.filter(actors__id__in=actors_ids)
    return qs.distinct()


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Iterable[int],
    actors_ids: Iterable[int]
) -> Movie:
    genres = Genre.objects.filter(id__in=genres_ids)
    if len(genres) != len(genres_ids):
        raise ValueError("Invalid genre ids")

    actors = Actor.objects.filter(id__in=actors_ids)
    if len(actors) != len(actors_ids):
        raise ValueError("Invalid actor ids")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )
    movie.genres.set(genres)
    movie.actors.set(actors)
    return movie
