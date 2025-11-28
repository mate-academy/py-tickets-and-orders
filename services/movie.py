from django.db.models import QuerySet
from django.db import transaction
from db.models import Movie


def get_movies(
    title: str | None = None,
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if title is not None:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(movie_title, movie_description, genres_ids, actors_ids):
    if not all(isinstance(i, int) for i in genres_ids):
        raise ValueError("Invalid genre ID")
    if not all(isinstance(i, int) for i in actors_ids):
        raise ValueError("Invalid actor ID")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )
    movie.genres.set(genres_ids)
    movie.actors.set(actors_ids)
    return movie

