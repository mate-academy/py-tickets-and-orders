from datetime import datetime

from django.db.models import QuerySet

from db.models import MovieSession, Ticket


def create_movie_session(
        movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    show_time = datetime.strptime(movie_show_time, "%Y-%m-%d %H:%M:%S")
    return MovieSession.objects.create(
        show_time=show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    queryset = MovieSession.objects.all()
    if session_date:
        session_date_obj = datetime.strptime(session_date, "%Y-%m-%d").date()
        queryset = queryset.filter(show_time__date=session_date_obj)
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


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list:
    movie_session = MovieSession.objects.get(id=movie_session_id)
    tickets = Ticket.objects.filter(movie_session=movie_session)
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in tickets]
