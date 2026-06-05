from datetime import datetime
from typing import Any, Optional

from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import MovieSession, Ticket


def create_movie_session(
    movie_show_time: str,
    movie_id: int,
    cinema_hall_id: int,
) -> MovieSession:
    """Create movie session."""
    show_time = parse_datetime(movie_show_time)
    if show_time is None:
        try:
            show_time = datetime.fromisoformat(
                movie_show_time.replace("Z", "+00:00")
            )
        except ValueError:
            show_time = datetime.fromisoformat(movie_show_time)

    return MovieSession.objects.create(
        show_time=show_time,  # type: ignore[attr-defined]
        movie_id=movie_id,    # type: ignore[attr-defined]
        cinema_hall_id=cinema_hall_id,  # type: ignore[attr-defined]
    )


def get_movies_sessions(
    session_date: Optional[str] = None
) -> QuerySet:
    """Return all movie sessions (with optional date filter)."""
    queryset = MovieSession.objects.all()
    if session_date:
        queryset = queryset.filter(show_time__date=session_date)
    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    """Return movie session by id."""
    return MovieSession.objects.get(id=movie_session_id)


def update_movie_session(
    session_id: int,
    show_time: Optional[str] = None,
    movie_id: Optional[int] = None,
    cinema_hall_id: Optional[int] = None,
) -> MovieSession:
    """Update movie session."""
    movie_session = MovieSession.objects.get(id=session_id)

    if show_time:
        dt = parse_datetime(show_time)
        if dt is None:
            try:
                dt = datetime.fromisoformat(
                    show_time.replace("Z", "+00:00")
                )
            except ValueError:
                dt = datetime.fromisoformat(show_time)
        movie_session.show_time = dt  # type: ignore[attr-defined]

    if movie_id is not None:
        movie_session.movie_id = movie_id  # type: ignore[attr-defined]
        movie_session.cinema_hall_id = (
    cinema_hall_id  # type: ignore[attr-defined]
 )
    movie_session.save()
    return movie_session


def delete_movie_session_by_id(session_id: int) -> None:
    """Delete movie session by id."""
    MovieSession.objects.filter(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list[dict[str, Any]]:
    """Return list of taken seats for the session."""
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [
        {"row": ticket.row, "seat": ticket.seat}
        for ticket in tickets
    ]
