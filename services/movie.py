from typing import Optional, Iterable
from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie, Genre, Actor


def get_movies(
    genres_ids: Optional[Iterable[int]] = None,
    actors_ids: Optional[Iterable[int]] = None,
    title: Optional[str] = None,
) -> QuerySet[Movie]:
    movies = Movie.objects.all()

    if title:
        movies = movies.filter(title__icontains=title)

    if genres_ids:
        movies = movies.filter(genres__id__in=genres_ids)

    if actors_ids:
        movies = movies.filter(actors__id__in=actors_ids)

    return movies.distinct()


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: Optional[str],
    genres_ids: Iterable[int],
    actors_ids: Iterable[int],
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description or "",
    )

    if genres_ids:
        genres = Genre.objects.filter(id__in=genres_ids)
        if genres.count() != len(genres_ids):
            raise Genre.DoesNotExist
        movie.genres.set(genres)

    if actors_ids:
        actors = Actor.objects.filter(id__in=actors_ids)
        if actors.count() != len(actors_ids):
            raise Actor.DoesNotExist
        movie.actors.set(actors)

    return movie
