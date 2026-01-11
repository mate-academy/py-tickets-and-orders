from django.db import transaction
from django.core.exceptions import ValidationError
from db.models import Movie, Genre, Actor
from django.db.models import QuerySet


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet:
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
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    genres_ids = genres_ids or []
    actors_ids = actors_ids or []

    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title, description=movie_description
        )

        genres = Genre.objects.filter(id__in=genres_ids)
        if len(genres) != len(genres_ids):
            missing_ids = set(genres_ids) - set(
                genres.values_list("id", flat=True)
            )
            raise ValidationError(f"Genres not found for IDs: {missing_ids}")

        actors = Actor.objects.filter(id__in=actors_ids)
        if len(actors) != len(actors_ids):
            missing_ids = set(actors_ids) - set(
                actors.values_list("id", flat=True)
            )
            raise ValidationError(f"Actors not found for IDs: {missing_ids}")

        movie.genres.set(genres)
        movie.actors.set(actors)

        return movie
