from django.db.models import QuerySet
from db.models import MovieSession


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)


def get_taken_seats(movie_session_id: int) -> list[dict]:
    tickets = MovieSession.objects.get(id=movie_session_id).tickets.all()
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
