from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model


@transaction.atomic()
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str | None = None) -> Order:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(
            user__username=username
        )
    return orders
