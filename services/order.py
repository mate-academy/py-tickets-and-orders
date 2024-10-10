from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"]
                              )

    order.save()
    return order


def get_orders(username: str = None) -> None:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
