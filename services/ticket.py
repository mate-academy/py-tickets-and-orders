from django.db.models import QuerySet
from db.models import Ticket


def create_ticket(
    order_id: int,
    movie_session_id: int,
    row: int,
    seat: int,
) -> Ticket:
    return Ticket.objects.create(
        order_id=order_id,
        movie_session_id=movie_session_id,
        row=row,
        seat=seat,
    )


def get_tickets(order_id: int) -> QuerySet[Ticket]:
    return Ticket.objects.filter(order_id=order_id)
