from django.db.models import QuerySet
from django.db import transaction
from db.models import Movie


def get_movies(
    title: str = None,
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
) -> QuerySet:
    movies_qs = Movie.objects.all()

    if title:
        movies_qs = movies_qs.filter(title__icontains=title)

    if genres_ids:
        movies_qs = movies_qs.filter(genres__id__in=genres_ids)

    if actors_ids:
        movies_qs = movies_qs.filter(actors__id__in=actors_ids)

    return movies_qs


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
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
    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
