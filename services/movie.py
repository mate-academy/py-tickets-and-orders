from typing import Optional, Any
from django.db import transaction, IntegrityError
from django.db.models import QuerySet
from db.models import Movie


@transaction.atomic
def create_movie(
    title: Optional[str] = None,
    description: Optional[str] = None,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
    **kwargs: Any
) -> Optional[Movie]:
    actual_title = title or kwargs.get("movie_title")

    try:
        movie = Movie.objects.create(
            title=actual_title,
            description=description
        )

        if genres_ids:
            movie.genres.set(genres_ids)
        if actors_ids:
            movie.actors.set(actors_ids)

        return movie
    except IntegrityError:
        raise ValueError("Invalid movie data")


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)
    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)
    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset.distinct().order_by("id")
