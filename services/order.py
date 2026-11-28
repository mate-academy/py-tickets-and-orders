from django.db import transaction
from db.models import Order, Ticket
from django.db.models import QuerySet
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None,
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
    if date is not None:
        order.created_at = date
    order.save()


def get_orders(
        username: str | None = None,
) -> QuerySet[Order]:
    if username is not None:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
