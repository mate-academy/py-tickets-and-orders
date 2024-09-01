from django.db import transaction

from db.models import Movie


def get_movies(
        title: str = None,
        genres_ids: int = None,
        actors_ids: int = None
) -> Movie:
    movies = Movie.objects.all()

    if title:
        movies = movies.filter(title__icontains=title)

    if genres_ids:
        movies = movies.filter(genres__id__in=genres_ids).distinct()

    if actors_ids:
        movies = movies.filter(actors__id__in=actors_ids).distinct()

    return movies


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
        movie_title: str,
        movie_description: str,
        genres_ids: list = None,
        actors_ids: list = None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )

        if genres_ids:
            if not all(isinstance(id, int) for id in genres_ids):
                raise ValueError("All genre IDs must be integers")
            movie.genres.set(genres_ids)

        if actors_ids:
            if not all(isinstance(id, int) for id in actors_ids):
                raise ValueError("All actor IDs must be integers")
            movie.actors.set(actors_ids)

        return movie
