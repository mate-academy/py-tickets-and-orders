from typing import List, Dict

from db.models import Ticket


def get_taken_seats(movie_session_id: int) -> List[Dict]:
    tickets = Ticket.objects.filter(
        movie_session_id=movie_session_id
    )

    return [
        {"row": ticket.row, "seat": ticket.seat}
        for ticket in tickets
    ]
