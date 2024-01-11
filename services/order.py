from django.db import transaction
from db.models import Order, Ticket, User
from typing import Optional, List


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: Optional[str] = None) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session = ticket_data.get("movie_session")

        Ticket.objects.create(
            row=row,
            seat=seat,
            movie_session_id=movie_session,
            order=order
        )


def get_orders(username: Optional[str] = None) -> List[Order]:
    if username is not None:
        return Order.objects.filter(user_id__username=username)
    return Order.objects.all()
