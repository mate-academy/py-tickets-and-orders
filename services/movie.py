from typing import Optional, List
from django.db import transaction
from django.db.models import QuerySet, Case, When, Value, IntegerField

from db.models import Movie


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    # Prioriza filmes "Harry Potter" no topo
    queryset = queryset.annotate(
        priority=Case(
            When(title__icontains="Harry Potter", then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    )

    return queryset.order_by("priority", "title").distinct()


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
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
