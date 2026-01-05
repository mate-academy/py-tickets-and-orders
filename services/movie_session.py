from typing import List, Optional, Dict
from datetime import date, datetime
from db.models import MovieSession, Ticket
from django.db.models import QuerySet
from django.db.models import Count, F


def create_movie_session(
    movie_show_time: datetime,
    movie_id: int,
    cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id
    )


def get_movies_sessions(
    session_date: Optional[date] = None,
    movie_id: Optional[int] = None
) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()

    if session_date:
        queryset = queryset.filter(show_time__date=session_date)

    if movie_id:
        queryset = queryset.filter(movie_id=movie_id)

    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: Optional[datetime] = None,
    movie_id: Optional[int] = None,
    cinema_hall_id: Optional[int] = None
) -> MovieSession:
    movie_session = MovieSession.objects.get(id=session_id)

    if show_time:
        movie_session.show_time = show_time

    if movie_id:
        movie_session.movie_id = movie_id

    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id

    movie_session.save()
    return movie_session


def delete_movie_session_by_id(session_id: int) -> None:
    movie_session = MovieSession.objects.get(id=session_id)
    movie_session.delete()


def get_taken_seats(movie_session_id: int) -> List[Dict[str, int]]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]


def get_movies_sessions_with_available_tickets(
    session_date: Optional[date] = None,
    movie_id: Optional[int] = None
) -> QuerySet[MovieSession]:
    return (
        get_movies_sessions(session_date=session_date, movie_id=movie_id)
        .annotate(
            tickets_available=(
                F("cinema_hall__capacity") - Count("tickets")
            )
        )
    )
