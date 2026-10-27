from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


def get_movies(title: str = None, genres_ids: list[int] = None, actors_ids: list[int] = None) -> QuerySet:
    """
    Повертає queryset фільмів.
    Опціонально фільтрує за title, genres_ids і actors_ids.
    """
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)
    
    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)
    
    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)
    
    return queryset.distinct()  # distinct потрібен, щоб уникнути дублікатів через M2M


def get_movie_by_id(movie_id: int) -> Movie:
    """
    Повертає об'єкт Movie за id
    """
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
) -> Movie:
    """
    Створює фільм у транзакції.
    Якщо genres_ids або actors_ids вказані, встановлює M2M зв'язки.
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
