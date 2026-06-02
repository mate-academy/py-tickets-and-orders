from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        Order.objects.filter(id=order.id).update(created_at=date)
        order.created_at = date

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    orders_queryset = Order.objects.select_related("user")

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset
