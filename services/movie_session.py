from typing import Optional, List, Dict
from datetime import datetime

from django.db.models import QuerySet
from db.models import MovieSession, Ticket


def get_movie_sessions(
        session_date: Optional[str] = None
) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()

    if session_date is not None:
        date_obj = datetime.strptime(
            session_date,
            "%Y-%m-%d"
        ).date()
        queryset = queryset.filter(
            show_time__date=date_obj
        )

    return queryset.select_related(
        "movie",
        "cinema_hall"
    )


def get_taken_seats(
        movie_session_id: int
) -> List[Dict]:
    return list(
        Ticket.objects.filter(
            movie_session_id=movie_session_id
        ).values(
            "row",
            "seat"
        ).order_by(
            "row",
            "seat"
        )
    )
