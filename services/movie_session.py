import datetime

from django.db.models import QuerySet

from db.models import MovieSession, Ticket


def create_movie_session(
    movie_show_time: datetime,
    movie_id: int,
    cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()

    if session_date:
        date = datetime.datetime.strptime(session_date, "%Y-%m-%d").date()
        queryset = queryset.filter(show_time__date=date)

    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: datetime = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    movie_session = MovieSession.objects.filter(id=session_id)

    if show_time:
        movie_session.update(show_time=show_time)

    if movie_id:
        movie_session.update(movie_id=movie_id)

    if cinema_hall_id:
        movie_session.update(cinema_hall_id=cinema_hall_id)


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.filter(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(
            movie_session_id=movie_session_id
        ).values("row", "seat")
    )
