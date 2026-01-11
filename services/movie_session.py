from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from db.models import MovieSession, Ticket


def create_movie_session(
        movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    queryset = MovieSession.objects.all()
    if session_date:
        try:
            queryset = queryset.filter(show_time__date=session_date)
        except ValueError:
            raise ValueError(f"Invalid date format: {session_date}. Expected format: YYYY-MM-DD")
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    try:
        return MovieSession.objects.get(id=movie_session_id)
    except MovieSession.DoesNotExist:
        raise ObjectDoesNotExist(f"MovieSession with id {movie_session_id} does not exist.")


def update_movie_session(
        session_id: int,
        show_time: str = None,
        movie_id: int = None,
        cinema_hall_id: int = None,
) -> None:
    try:
        movie_session = MovieSession.objects.get(id=session_id)
    except MovieSession.DoesNotExist:
        raise ObjectDoesNotExist(f"MovieSession with id {session_id} does not exist.")

    if show_time:
        movie_session.show_time = show_time
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id
    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    try:
        MovieSession.objects.get(id=session_id).delete()
    except MovieSession.DoesNotExist:
        raise ValueError(f"MovieSession with id {session_id} does not exist.")


def get_taken_seats(movie_session_id: int) -> list[dict]:
    taken_seats = (Ticket.objects.filter(movie_session_id=movie_session_id)
                   .values("row", "seat"))
    return list(taken_seats)
