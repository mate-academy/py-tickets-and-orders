from __future__ import annotations

from typing import Dict, List

from db.models import Ticket


def get_taken_seats(movie_session_id: int) -> List[Dict[str, int]]:
    """
    Retorna a lista de assentos já ocupados para uma sessão específica,
    no formato: [{"row": 7, "seat": 10}, ...].
    """
    return list(
        Ticket.objects.filter(movie_session_id=movie_session_id)
        .values("row", "seat")
        .order_by("row", "seat")
    )
