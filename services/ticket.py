from db.models import Ticket
from services.movie_session import get_movie_session_by_id


def create_ticket(
    movie_session_id: int,
    order_id: int,
    row: int,
    seat: int,
) -> Ticket:
    this_movie_session = get_movie_session_by_id(movie_session_id)
    new_ticket = Ticket.objects.create(
        movie_session=this_movie_session,
        order_id=order_id,
        row=row,
        seat=seat,
    )
    return new_ticket
