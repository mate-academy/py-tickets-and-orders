from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None, title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(movie_title: str,
                 movie_description: str,
                 genres_ids: list[int],
                 actors_ids: list[int]) -> Movie:
    with transaction.atomic():
        if not genres_ids:
            raise ValueError("Genres list cannot be empty")
        if not actors_ids:
            raise ValueError("Actors list cannot be empty")

        movie = Movie.objects.create(title=movie_title,
                                     description=movie_description)
        movie.genres.set(genres_ids)
        movie.actors.set(actors_ids)
        return movie
