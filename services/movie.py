from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie, Genre, Actor


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    try:
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description
        )

        genres = Genre.objects.filter(id__in=genres_ids)
        actors = Actor.objects.filter(id__in=actors_ids)

        if genres.count() != len(genres_ids):
            raise ValueError("One or more genre IDs are invalid.")

        if actors.count() != len(actors_ids):
            raise ValueError("One or more actor IDs are invalid.")

        # Assign genres and actors to the movie
        movie.genres.set(genres)
        movie.actors.set(actors)
        movie.save()
    except ValueError as e:
        raise e
    except Exception as e:
        raise e
