from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | None = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    qs = Order.objects.select_related("user")
    if username:
        qs = qs.filter(user__username=username)
    return qs
