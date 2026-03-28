from django.db import transaction

from django.db.models import QuerySet

from db.models import Movie, Genre, Actor


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
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
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    try:
        with transaction.atomic():
            if genres_ids:
                genres = Genre.objects.filter(id__in=genres_ids)
                movie.genres.set(genres)
            if actors_ids:
                actors = Actor.objects.filter(id__in=actors_ids)
                movie.actors.set(actors)
    except ValueError as e:
        movie.delete()
        raise e

    return movie
