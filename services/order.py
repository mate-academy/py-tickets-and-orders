from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session = ticket_data.get("movie_session")
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        ticket = Ticket(
            movie_session_id=movie_session,
            order=order,
            row=row,
            seat=seat
        )

        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)
    return orders
