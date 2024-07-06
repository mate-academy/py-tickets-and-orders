from django.db.models import QuerySet

from db.models import MovieSession


def get_taken_seats(movie_session_id: int) -> QuerySet:
    movie_session = MovieSession.objects.get(id=movie_session_id)
    tickets = movie_session.ticket_set.all()
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
