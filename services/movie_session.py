from django.db.models import QuerySet

from db.models import MovieSession
from db.models import MovieSession, Ticket


def create_movie_session(
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
def get_movies_sessions(session_date: str = None) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)

def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(
            movie_session_id=movie_session_id
        ).values("row", "seat")
    )