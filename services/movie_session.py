from django.db.models import QuerySet
from typing import Optional
from datetime import datetime

from db.models import MovieSession, Movie, CinemaHall, Ticket


def create_movie_session(
        movie_show_time: str,
        movie_id: int,
        cinema_hall_id: int
) -> MovieSession:
    show_time = datetime.fromisoformat(movie_show_time)
    movie = Movie.objects.get(id=movie_id)
    cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)

    return MovieSession.objects.create(
        show_time=show_time,
        movie=movie,
        cinema_hall=cinema_hall,
    )


def create_multiple_movie_sessions(
        sessions_data: list[dict]
) -> list[MovieSession]:
    """
    Optimized function to create multiple movie sessions efficiently,
    avoiding N+1 query problems by fetching all movies and cinema halls
    upfront.
    """
    if not sessions_data:
        return []

    movie_ids = {
        session_data["movie_id"] for session_data in sessions_data
    }
    cinema_hall_ids = {
        session_data["cinema_hall_id"] for session_data in sessions_data
    }

    movies = {
        movie.pk: movie for movie in Movie.objects.filter(id__in=movie_ids)
    }
    cinema_halls = {
        hall.pk: hall
        for hall in CinemaHall.objects.filter(id__in=cinema_hall_ids)
    }

    sessions = []
    for session_data in sessions_data:
        show_time = datetime.fromisoformat(session_data["movie_show_time"])
        movie = movies[session_data["movie_id"]]
        cinema_hall = cinema_halls[session_data["cinema_hall_id"]]

        session = MovieSession.objects.create(
            show_time=show_time,
            movie=movie,
            cinema_hall=cinema_hall,
        )
        sessions.append(session)

    return sessions


def get_movies_sessions(
        session_date: Optional[str] = None,
        movie_id: Optional[int] = None
) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    if movie_id:
        queryset = queryset.filter(movie_id=movie_id)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
        session_id: int,
        show_time: Optional[str] = None,
        movie_id: Optional[int] = None,
        cinema_hall_id: Optional[int] = None,
) -> MovieSession:
    movie_session = MovieSession.objects.get(id=session_id)

    if show_time:
        movie_session.show_time = datetime.fromisoformat(show_time)
    if movie_id:
        movie_session.movie = Movie.objects.get(id=movie_id)
    if cinema_hall_id:
        movie_session.cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)

    movie_session.save()
    return movie_session


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
    )
