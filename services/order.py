from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: datetime | None = None,
) -> Order:

    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
