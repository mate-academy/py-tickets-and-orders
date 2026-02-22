from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None
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


def create_movie(
    movie_title: str,
    movie_description: str,
    movie_duration: int,
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
) -> Movie:
    if genres_ids is not None:
        if (not isinstance(genres_ids, list)
                or not all(isinstance(g, int) for g in genres_ids)):
            raise ValueError("Genres must be a list of integers.")

    if actors_ids is not None:
        if (not isinstance(actors_ids, list)
                or not all(isinstance(a, int) for a in actors_ids)):
            raise ValueError("Actors must be a list of integers.")

    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
            duration=movie_duration,
        )
        if genres_ids:
            movie.genres.set(genres_ids)
        if actors_ids:
            movie.actors.set(actors_ids)

    return movie
