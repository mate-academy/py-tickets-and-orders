from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order(user=user)

    if date is not None:
        order.created_at = date
        Order._meta.get_field("created_at").auto_now_add = False
        order.save()
        Order._meta.get_field("created_at").auto_now_add = True
    else:
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
