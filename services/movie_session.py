import datetime
from db.models import Movie
from db.models import CinemaHall
from db.models import MovieSession, Ticket


def create_movie_session(
    movie: Movie, cinema_hall: CinemaHall, show_time: datetime
) -> MovieSession:
    movie_session = MovieSession.objects.create(
        movie=movie,
        cinema_hall=cinema_hall,
        show_time=show_time,
    )
    return movie_session


def update_movie_session(
    session_id: int, **kwargs
) -> MovieSession:
    movie_session = MovieSession.objects.get(id=session_id)
    for key, value in kwargs.items():
        setattr(movie_session, key, value)
    movie_session.save()
    return movie_session


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id).values(
            "row", "seat"
        )
    )
