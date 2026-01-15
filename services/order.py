from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str, date: Optional[str] = None) -> None:
    user = get_user_model()

    user = user.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
        order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
