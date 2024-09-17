from typing import Optional
from django.db.models import QuerySet
from db.models import Ticket
from db.models import MovieSession, CinemaHall, Movie


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(
        session_date: Optional[str] = None
) -> QuerySet:

    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: Optional[str] = None,
    cinema_hall: Optional[CinemaHall] = None,
    movie: Optional[Movie] = None
) -> None:

    movie_session = MovieSession.objects.get(id=session_id)
    if show_time:
        movie_session.show_time = show_time
    if cinema_hall:
        movie_session.cinema_hall = cinema_hall
    if movie:
        movie_session.movie = movie
    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
