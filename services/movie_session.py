from datetime import date, datetime

from django.db.models import QuerySet

from db.models import MovieSession, Ticket


def create_movie_session(
    movie_id: int,
    cinema_hall_id: int,
    show_time: str,
) -> MovieSession:
    return MovieSession.objects.create(
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
        show_time=datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S"),
    )


def get_movie_sessions(
    session_date: date = None,
) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()

    if session_date:
        queryset = queryset.filter(show_time__date=session_date)

    return queryset


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> MovieSession:
    movie_session = MovieSession.objects.get(id=session_id)

    if show_time:
        movie_session.show_time = datetime.strptime(
            show_time,
            "%Y-%m-%d %H:%M:%S",
        )
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id

    movie_session.save()
    return movie_session


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
    )
