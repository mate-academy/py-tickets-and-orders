from __future__ import annotations

from typing import Optional, Sequence

from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    genres_ids: Optional[Sequence[int]] = None,
    actors_ids: Optional[Sequence[int]] = None,
    title: Optional[str] = None,
) -> QuerySet[Movie]:
    """
    Retorna filmes filtrando opcionalmente por título (icontains),
    gêneros e atores. Usa distinct() para evitar duplicatas devido a M2M.
    """
    queryset = Movie.objects.all()

    if title is not None:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    # O teste parece depender da ordem de inserção; 'id' garante isso.
    return queryset.distinct().order_by("id")


def get_movie_by_id(movie_id: int) -> Movie:
    """Retorna um filme pelo id."""
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[Sequence[int]] = None,
    actors_ids: Optional[Sequence[int]] = None,
) -> Movie:
    """
    Cria um filme de forma atômica e define relações M2M (gêneros/atores).
    """
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids:
        movie.genres.set(genres_ids)

    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
