from db.models import Ticket


def get_taken_seats(movie_session_id: int) -> list[dict]:
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
    )
