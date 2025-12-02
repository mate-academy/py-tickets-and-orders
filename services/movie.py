from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
        genres_ids: list | None = None,
        actors_ids: list | None = None,
        title: str | None = None
) -> QuerySet:
    movies = Movie.objects.all()

    if title is not None:
        movies = movies.filter(title__icontains=title)

    if genres_ids is not None:
        movies = movies.filter(genres__id__in=genres_ids).distinct()

    if actors_ids is not None:
        movies = movies.filter(actors__id__in=actors_ids).distinct()

    return movies


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list | None = None,
    actors_ids: list | None = None
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )

        if genres_ids:
            if not all(isinstance(i, int) for i in genres_ids):
                raise ValueError("All genre IDs must be integers")
            movie.genres.set(genres_ids)

        if actors_ids:
            if not all(isinstance(i, int) for i in actors_ids):
                raise ValueError("All actor IDs must be integers")
            movie.actors.set(actors_ids)

    return movie
