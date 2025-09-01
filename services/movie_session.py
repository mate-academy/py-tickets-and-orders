from db.models import Ticket


def get_taken_seats(movie_session_id: int) -> list[dict]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": t.row, "seat": t.seat} for t in tickets]
