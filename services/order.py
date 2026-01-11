from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model
from typing import List, Dict

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: List[Dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )

    return order


def get_orders(username: str = None) -> List[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
