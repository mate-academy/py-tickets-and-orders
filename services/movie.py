from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    title: str = None,
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
) -> QuerySet[Movie]:
    movies = Movie.objects.all()

    if title:
        movies = movies.filter(title__icontains=title)
    if genres_ids:
        movies = movies.filter(genres__id__in=genres_ids)
    if actors_ids:
        movies = movies.filter(actors__id__in=actors_ids)

    return movies


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> None:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    movie.save()
