from typing import Optional
from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


@transaction.atomic
def create_movie(
    title: str,
    description: str = None,
    release_date = None,
) -> Movie:
    movie = Movie.objects.create(
        title=title,
        description=description,
        release_date=release_date,
    )
    return movie


def get_movies(
    title: Optional[str] = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()
    if title is not None:
        queryset = queryset.filter(title__icontains=title)
    return queryset
