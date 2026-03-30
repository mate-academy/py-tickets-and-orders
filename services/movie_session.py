from typing import List, Dict

from db.models import MovieSession, Ticket


def get_movie_session_by_id(session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=session_id)


def get_taken_seats(movie_session_id: int) -> List[Dict[str, int]]:
    session = get_movie_session_by_id(movie_session_id)
    tickets = Ticket.objects.filter(movie_session=session)

    return [
        {"row": t.row, "seat": t.seat}
        for t in tickets
    ]
