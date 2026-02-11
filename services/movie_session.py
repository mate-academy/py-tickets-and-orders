from django.db import transaction
from django.db.models import QuerySet
from db.models import MovieSession


@transaction.atomic
def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    """
    Створює MovieSession в транзакції
    """
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    """
    Повертає queryset всіх сеансів.
    Якщо передано session_date, фільтрує за датою.
    """
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    """
    Повертає об'єкт MovieSession за id
    """
    return MovieSession.objects.get(id=movie_session_id)


@transaction.atomic
def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    """
    Оновлює MovieSession
    """
    movie_session = MovieSession.objects.get(id=session_id)
    if show_time:
        movie_session.show_time = show_time
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id
    movie_session.save()


@transaction.atomic
def delete_movie_session_by_id(session_id: int) -> None:
    """
    Видаляє MovieSession за id
    """
    MovieSession.objects.get(id=session_id).delete()
