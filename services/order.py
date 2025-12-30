from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, MovieSession

from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
        )


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()

    if username:
        return orders.filter(user__username=username)

    return orders
