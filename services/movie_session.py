from django.db.models import QuerySet
from db.models import MovieSession, Ticket


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    qs = MovieSession.objects.all()
    if session_date:
        qs = qs.filter(show_time__date=session_date)
    return qs


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    ms = MovieSession.objects.get(id=session_id)
    if show_time:
        ms.show_time = show_time
    if movie_id:
        ms.movie_id = movie_id
    if cinema_hall_id:
        ms.cinema_hall_id = cinema_hall_id
    ms.save()


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict[str, int]]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": t.row, "seat": t.seat} for t in tickets]
