from db.models import Movie
from django.db import transaction


def get_movies(genres_ids=None, actors_ids=None, title=None) -> models.QuerySet:
    movies = Movie.objects.all()
    if genres_ids:
        movies = movies.filter(genres__id__in=genres_ids)
    if actors_ids:
        movies = movies.filter(actors__id__in=actors_ids)
    if title:
        movies = movies.filter(title__icontains=title)
    return movies.distinct().order_by("id")


@transaction.atomic
def create_movie(movie_title, movie_description, genres_ids, actors_ids) -> Movie:
    movie = Movie.objects.create(title=movie_title, description=movie_description)
    movie.genres.set(genres_ids)
    movie.actors.set(actors_ids)
    return movie
