from django.db.models import QuerySet
from db.models import Movie


def get_movies(
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None,
    title: str | None = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if genres_ids is not None:
        if not genres_ids:
            return Movie.objects.none()
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids is not None:
        if not actors_ids:
            return Movie.objects.none()
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title is not None:
        if title == "":
            return Movie.objects.none()
        queryset = queryset.filter(title__icontains=title)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids is not None:
        movie.genres.set(genres_ids)
    if actors_ids is not None:
        movie.actors.set(actors_ids)

    return movie
