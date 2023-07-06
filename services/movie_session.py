from django.db.models import QuerySet, F

from db.models import MovieSession


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> None:
    MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(
    session_date: str = None
) -> QuerySet[MovieSession]:
    sessions = MovieSession.objects.all()

    if session_date:
        sessions = sessions.filter(show_time__date=session_date)

    return sessions


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    **kwargs,
) -> None:
    movie_session = get_movie_session_by_id(session_id)
    fields = ["show_time", "cinema_hall", "movie"]

    for field, data in kwargs.items():
        if data and field in fields:
            setattr(movie_session, field, data)

    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    get_movie_session_by_id(session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(MovieSession.objects.filter(
        id=movie_session_id).values(
            row=F("tickets__row"),
            seat=F("tickets__seat")
    ))
