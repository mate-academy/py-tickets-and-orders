from typing import List, Dict, Any
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: List[Dict[str, Any]],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session,
        )
    return order


def get_orders(username: str = None) -> List[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
