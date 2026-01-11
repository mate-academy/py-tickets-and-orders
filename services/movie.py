from typing import Optional, List
from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)
    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids).distinct()
    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids).distinct()

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
) -> Movie:
    if genres_ids:
        for genre_id in genres_ids:
            if not isinstance(genre_id, int):
                raise ValueError("Invalid genre id")

    if actors_ids:
        for actor_id in actors_ids:
            if not isinstance(actor_id, int):
                raise ValueError("Invalid actor id")

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
