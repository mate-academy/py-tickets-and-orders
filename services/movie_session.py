from typing import List

from django.db.models import QuerySet
from db.models import MovieSession, Ticket
from django.core.exceptions import ValidationError
from datetime import datetime


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
        date_obj = datetime.strptime(session_date, "%Y-%m-%d").date()
        queryset = queryset.filter(show_time__date=date_obj)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    movie_session = MovieSession.objects.get(id=session_id)
    if show_time:
        movie_session.show_time = show_time
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id
    movie_session.save()


def get_taken_seats(movie_session_id: int) -> List[dict]:
    """
    Fetches a list of taken seats for a given movie session.

    Args:
        movie_session_id (int): The ID of the movie session.

    Returns:
        list of dict: A list of dictionaries,
        each representing a taken seat
        with its row and seat number.
    """
    if not isinstance(movie_session_id, int):
        raise ValidationError("Invalid movie session ID")

    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)

    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
