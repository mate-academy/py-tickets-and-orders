# db/services/movie.py
from django.db import transaction
from db.models import Movie


def get_movies(title: str = None):
    movies = Movie.objects.all()
    if title:
        movies = movies.filter(title__icontains=title)
    return movies


@transaction.atomic
def create_movie(title: str, description: str, duration: int):
    movie = Movie.objects.create(
        title=title, description=description, duration=duration
    )
    return movie
