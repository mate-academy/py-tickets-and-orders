from typing import Optional

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import MovieSession, Ticket


def create_movie_session(
        movie_show_time: str,
        cinema_hall_id: int,
        movie_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=movie_show_time,
        cinema_hall_id=cinema_hall_id,
        movie_id=movie_id
    )


def get_movies_sessions(
        session_date: Optional[str] = None,
) -> QuerySet:
    queryset = MovieSession.objects.all()

    if session_date:
        queryset = queryset.filter(
            show_time__date=session_date
        )

    return queryset


def get_movie_session_by_id(movie_session_id: int) -> MovieSession:
    return get_object_or_404(
        MovieSession,
        id=movie_session_id
    )


def update_movie_session(
        session_id: int,
        show_time: Optional[str] = None,
        movie_id: Optional[str] = None,
        cinema_hall_id: Optional[str] = None,
) -> MovieSession:
    movie_session_to_update = get_object_or_404(
        MovieSession,
        id=session_id
    )

    if show_time:
        movie_session_to_update.show_time = show_time

    if movie_id:
        movie_session_to_update.movie_id = movie_id

    if cinema_hall_id:
        movie_session_to_update.cinema_hall_id = cinema_hall_id

    movie_session_to_update.save()

    return movie_session_to_update


def delete_movie_session_by_id(session_id: int) -> int:
    movie_session_to_delete = get_movie_session_by_id(session_id)

    return movie_session_to_delete.delete()


def get_taken_seats(movie_session_id: int) -> list[dict[str, int]]:
    return [
        {"row": ticket.row, "seat": ticket.seat}
        for ticket in Ticket.objects.filter(
            movie_session_id=movie_session_id
        )
        .select_related("movie_session")
    ]
