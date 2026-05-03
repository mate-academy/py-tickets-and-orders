from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict] = None,
        username: str = None,
        date: str = None,
) -> Order:

    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )

    return order


def get_orders(
        username: str = None,
) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
