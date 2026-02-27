from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from db.models import MovieSession, Ticket
from django.core.exceptions import ObjectDoesNotExist


def create_movie_session(
        movie_show_time: str,
        movie_id: int,
        cinema_hall_id: int) -> MovieSession:
    """
    Create a new movie session.
    """
    return MovieSession.objects.create(
        show_time=movie_show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )


def get_movies_sessions(
        session_date: str = None) -> QuerySet:
    """
    Retrieve movie sessions, optionally filtered by date.
    """
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(
        movie_session_id: int) -> MovieSession:
    """
    Retrieve a movie session by its ID.
    """
    return get_object_or_404(MovieSession, id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: str = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> None:
    """
    Update a movie session's details.
    """
    try:
        movie_session = MovieSession.objects.get(id=session_id)
        if show_time:
            movie_session.show_time = show_time
        if movie_id:
            movie_session.movie_id = movie_id
        if cinema_hall_id:
            movie_session.cinema_hall_id = cinema_hall_id
        movie_session.save()
    except ObjectDoesNotExist:
        raise ValueError(
            f"Movie session with ID {session_id} does not exist.")


def delete_movie_session_by_id(session_id: int) -> None:
    """
    Delete a movie session by its ID.
    """
    try:
        MovieSession.objects.get(id=session_id).delete()
    except ObjectDoesNotExist:
        raise ValueError(
            f"Movie session with ID {session_id} does not exist.")


def get_taken_seats(
        movie_session_id: int) -> list[dict[str, int]]:
    """
    Retrieve the taken seats for a given movie session.
    Returns a list of dictionaries with rows and seats.
    """
    tickets = Ticket.objects.filter(
        movie_session_id=movie_session_id).values("row", "seat")
    return list(tickets)
