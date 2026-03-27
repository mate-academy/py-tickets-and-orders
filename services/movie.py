from django.db.models import QuerySet
from django.db import transaction
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet[Movie]:
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


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    movie = Movie(title=movie_title, description=movie_description)
    movie.save()

    if genres_ids:
        if not all(isinstance(g, int) for g in genres_ids):
            raise ValueError("genres_ids must be integers")
        movie.genres.set(genres_ids)
    if actors_ids:
        if not all(isinstance(a, int) for a in actors_ids):
            raise ValueError("actors_ids must be integers")
        movie.actors.set(actors_ids)
    return movie
