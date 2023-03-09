from typing import List

from db.models import MovieSession, Ticket


def create_movie_session(
        movie_show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> MovieSession:
    movie_session = MovieSession.objects.all()

    if session_date:
        movie_session = movie_session.filter(show_time__date=session_date)

    return movie_session


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(session_id: int, **kwargs) -> None:
    movie_session = MovieSession.objects.get(id=session_id)

    for key, value in kwargs.items():
        setattr(movie_session, key, value)

    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> List[dict]:
    movie_session = MovieSession.objects.get(id=movie_session_id)

    tickets = Ticket.objects.filter(movie_session=movie_session).values_list(
        "row", "seat")

    return [{"row": ticket[0], "seat": ticket[1]} for ticket in tickets]
