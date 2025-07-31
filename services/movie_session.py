from typing import Optional

from django.db.models import QuerySet

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
    sessions_qs = MovieSession.objects.all()
    if session_date:
        sessions_qs = sessions_qs.filter(show_time__date=session_date)
    return sessions_qs


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: Optional[str] = None,
    movie_id: Optional[int] = None,
    cinema_hall_id: Optional[int] = None,
) -> None:
    session_obj = MovieSession.objects.get(id=session_id)
    if show_time:
        session_obj.show_time = show_time
    if movie_id:
        session_obj.movie_id = movie_id
    if cinema_hall_id:
        session_obj.cinema_hall_id = cinema_hall_id
    session_obj.save()


def delete_movie_session_by_id(session_id: int) -> Optional[MovieSession]:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict[str, int]]:
    taken_seats = (
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
    )
    return list(taken_seats)
