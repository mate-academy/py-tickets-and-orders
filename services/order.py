from typing import List, Dict, Optional
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]], username: str, date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    ticket_objects: List[Ticket] = [
        Ticket(
            order=order,
            row=data["row"],
            seat=data["seat"],
            movie_session=MovieSession.objects.get(id=data["movie_session"]),
        )
        for data in tickets
    ]

    if date:
        order.created_at = date
        order.save()

    Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(username: Optional[str] = None) -> List[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
