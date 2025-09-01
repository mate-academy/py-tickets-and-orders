from db.models import Movie
from django.db import transaction
from typing import Optional, List


def get_movies(title: Optional[str] = None) -> List[Movie]:
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    return qs


@transaction.atomic
def create_movie(
    title: str,
    description: Optional[str] = None,
    duration: Optional[int] = None
) -> Movie:
    movie = Movie(title=title, description=description, duration=duration)
    movie.save()
    return movie
