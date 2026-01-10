# db/services/movie_session.py
from db.models import MovieSession, Ticket


def get_taken_seats(movie_session_id: int):
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
