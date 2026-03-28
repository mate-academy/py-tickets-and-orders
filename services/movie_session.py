from django.db.models import QuerySet
from db.models import MovieSession
from typing import List, Dict
from db.models import Ticket


def create_movie_session(
    movie_show_time: str,
    movie_id: int,
    cinema_hall_id: int,
) -> MovieSession:
    """Create a new movie session."""
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(session_date: str = None) -> QuerySet:
    """Retrieve movie sessions, optionally filtered by session_date."""
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    """Get a movie session by its ID."""
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    """Update an existing movie session."""
    movie_session = MovieSession.objects.get(id=session_id)
    if show_time:
        movie_session.show_time = show_time
    if movie_id:
        movie_session.movie_id = movie_id
    if cinema_hall_id:
        movie_session.cinema_hall_id = cinema_hall_id
    movie_session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    """Delete a movie session by its ID."""
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> List[Dict[str, int]]:
    """
    Get a list of taken seats for a given movie session.

    :param movie_session_id: The ID of the movie session.
    :return: A list of dictionaries with rows and seats of the taken tickets.
    """
    taken_seats = Ticket.objects.filter(
        movie_session_id=movie_session_id
    ).values("row", "seat")
    return list(taken_seats)

# Ensure there is a newline at the end of the file
