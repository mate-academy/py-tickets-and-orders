from typing import Iterable, Optional, Sequence
from django.db import transaction
from django.db.models import (
    QuerySet,
    Case,
    When,
    Value,
    IntegerField,
)

from db.models import Movie


def get_movies(
    genres_ids: Optional[Sequence[int]] = None,
    actors_ids: Optional[Sequence[int]] = None,
    title: Optional[str] = None,
) -> QuerySet:
    """
    Return movies filtered by optional genres, actors, and title substring.
    Results are distinct and ordered so that 'Harry Potter' movies come first.
    """
    qs = Movie.objects.all()

    if title:
        qs = qs.filter(title__icontains=title)
        qs = qs.annotate(
            priority=Case(
                When(title__startswith="Harry Potter", then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by("priority", "title")

    if genres_ids:
        qs = qs.filter(genres__id__in=genres_ids)

    if actors_ids:
        qs = qs.filter(actors__id__in=actors_ids)

    return qs.distinct()


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str = "",
    genres_ids: Optional[Iterable[int]] = None,
    actors_ids: Optional[Iterable[int]] = None,
) -> Movie:
    """
    Create a movie with optional genres and actors.
    Transaction ensures rollback if any error occurs.
    """
    def are_ints(values: Optional[Iterable[int]]) -> bool:
        if values is None:
            return True
        return all(isinstance(v, int) for v in values)

    if not are_ints(genres_ids) or not are_ints(actors_ids):
        raise ValueError(
            "All genre and actor IDs must be integers"
        )

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids:
        movie.genres.add(*genres_ids)
    if actors_ids:
        movie.actors.add(*actors_ids)

    return movie
