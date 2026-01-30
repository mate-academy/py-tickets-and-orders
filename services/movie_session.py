from typing import List, Dict

from db.models import Ticket


def get_taken_seats(*, movie_session_id: int) -> List[Dict[str, int]]:
    tickets = Ticket.objects.filter(movie_session_id=movie_session_id).values(
        "row", "seat"
    )
    return [{"row": t["row"], "seat": t["seat"]} for t in tickets]
