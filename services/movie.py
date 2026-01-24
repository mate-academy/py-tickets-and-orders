from typing import Any, Optional, List
from django.db import transaction
from db.models import Movie


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
) -> Any:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

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
    genres_ids: List[int],
    actors_ids: List[int]
) -> Movie:
    with transaction.atomic():
        if not isinstance(genres_ids, list) or not all(isinstance(
                i, int) for i in genres_ids):
            raise ValueError("Genres should be a list of integers")

        if not isinstance(actors_ids, list) or not all(isinstance(
                i, int) for i in actors_ids):
            raise ValueError("Actors should be a list of integers")

        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description
        )

        movie.genres.set(genres_ids)
        movie.actors.set(actors_ids)

        return movie
