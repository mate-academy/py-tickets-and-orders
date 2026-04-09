from django.db.models import QuerySet
from typing import Optional, List
from django.db import transaction
from db.models import Movie, Actor, Genre


def get_movies(
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
    title: Optional[str] = None,
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
    actors_ids: Optional[List[int]] = None,
    genres_ids: Optional[List[int]] = None,
) -> Movie:
    if genres_ids and not all(isinstance(gid, int) for gid in genres_ids):
        raise ValueError("All genres_ids must be integers")
    if actors_ids and not all(isinstance(aid, int) for aid in actors_ids):
        raise ValueError("All actors_ids must be integers")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if actors_ids:
        actors = Actor.objects.filter(id__in=actors_ids)
        movie.actors.set(actors)

    if genres_ids:
        genres = Genre.objects.filter(id__in=genres_ids)
        movie.genres.set(genres)

    return movie
