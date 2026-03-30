from typing import Optional
from db.models import MovieSession, Ticket


def get_movie_session(movie_session_id: int) -> Optional[MovieSession]:
    return MovieSession.objects.filter(id=movie_session_id).first()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return list(tickets.values("row", "seat"))
