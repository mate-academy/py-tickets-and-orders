from db.models import Ticket


def get_taken_seats(movie_session_id)-> List[Dict[str, int]]:
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
        .order_by("row", "seat")
    )
