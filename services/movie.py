from db.models import Movie, Genre, Actor
from django.db import transaction, models
from typing import List, Optional


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None
) -> models.QuerySet[Movie]:
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    if genres_ids:
        qs = qs.filter(genres__id__in=genres_ids)
    if actors_ids:
        qs = qs.filter(actors__id__in=actors_ids)
    return qs.distinct().order_by("id")


@transaction.atomic
def create_movie(
    title: str,
    description: str,
    duration: int,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None
) -> Movie:
    movie = Movie.objects.create(
        title=title,
        description=description,
        duration=duration
    )

    if genres_ids:
        genres = Genre.objects.filter(id__in=genres_ids)
        movie.genres.set(genres)

    if actors_ids:
        actors = Actor.objects.filter(id__in=actors_ids)
        movie.actors.set(actors)

    return movie
