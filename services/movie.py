from typing import List, Optional

from django.db.models import QuerySet

from db.models import Movie, Genre, Actor


def get_movies(title: Optional[str] = None,
               genres_ids: Optional[List[int]] = None,
               actors_ids: Optional[List[int]] = None) -> QuerySet:

    """
    Fetches a list of movies based on the given filters.

    Args:
        title (str): The title of the movie to search for.
        genres_ids (list): A list of genre IDs to filter by.
        actors_ids (list): A list of actor IDs to filter by.

    Returns:
        QuerySet: A Django QuerySet of filtered movies.
    """
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
    genres_ids: Optional[List[int]] = None,
    actors_ids: Optional[List[int]] = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids:
        genres = Genre.objects.filter(id__in=genres_ids)
        movie.genres.set(genres)
    if actors_ids:
        actors = Actor.objects.filter(id__in=actors_ids)
        movie.actors.set(actors)

    return movie
