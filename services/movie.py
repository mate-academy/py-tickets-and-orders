from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all().prefetch_related("genres", "actors")

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    actors: list[int] = None,
    genres: list[int] = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title, description=movie_description
    )
    if actors:
        movie.actors.set(actors)
    if genres:
        movie.genres.set(genres)
    return movie
