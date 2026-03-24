from typing import List
from django.db.models import QuerySet
from db.models import MovieSession, Ticket


def get_movies_sessions(
        session_date: str | None = None) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def get_taken_seats(movie_session_id: int) -> List[dict]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": t.row, "seat": t.seat} for t in tickets]
