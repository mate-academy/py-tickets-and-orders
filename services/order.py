from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket
from datetime import datetime
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        parsed = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.pk).update(created_at=parsed)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
