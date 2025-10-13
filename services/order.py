from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime


User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | None = None
) -> Order:
    user = User.objects.get(username=username)
    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        ticket_created = Ticket(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
        ticket_created.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        filter_order = Order.objects.filter(user__username=username)
        return filter_order.prefetch_related("tickets")
    return Order.objects.all().prefetch_related("tickets")
