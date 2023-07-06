from django.db.models import QuerySet

from db.models import MovieSession


def create_movie_session(
    movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> None:
    MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    **kwargs
) -> None:
    movie_session = MovieSession.objects.get(id=session_id)

    for attr, value in kwargs.items():
        if attr in ["show_time", "movie_id", "cinema_hall_id"]:
            setattr(movie_session, attr, value)
    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        MovieSession.objects.get(
            id=movie_session_id
        ).tickets.values("row", "seat")
    )
