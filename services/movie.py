from typing import Optional, List
from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


def get_movies(
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
    title: Optional[str] = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if genres_ids or actors_ids:
        queryset = queryset.distinct()

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
    duration: Optional[int] = None,
) -> Movie:
    defaults = {
        "title": movie_title,
        "description": movie_description,
    }
    if duration is not None:
        defaults["duration"] = duration

    movie = Movie.objects.create(**defaults)

    if genres_ids:
        movie.genres.set(genres_ids)

    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
