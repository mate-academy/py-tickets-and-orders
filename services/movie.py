from django.db.models import QuerySet
from django.db import transaction
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None  # Добавляем аргумент title
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:  # Проверяем, если передан аргумент title
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
        # Создаем фильм
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )

        # Устанавливаем жанры фильма
        if genres_ids:
            movie.genres.set(genres_ids)

        # Устанавливаем актеров фильма
        if actors_ids:
            movie.actors.set(actors_ids)

        return movie
    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        transaction.set_rollback(True)
        raise e
