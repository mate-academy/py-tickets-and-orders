from db.models import Ticket
from typing import List, Dict, Any


def get_taken_seats(movie_session_id: int) -> List[Dict[str, Any]]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id)
    return [{"row": t.row, "seat": t.seat} for t in tickets]
