from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from django.db import transaction
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(
        user=user
    )

    if date:
        date_format = "%Y-%m-%d %H:%M"
        order.created_at = datetime.strptime(date, date_format)
        order.save()

    tickets_to_create = []
    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session_id = ticket_data.get("movie_session")

        ticket = Ticket(
            movie_session_id=movie_session_id,
            order=order,
            row=row,
            seat=seat
        )

        ticket.full_clean()

        tickets_to_create.append(
            ticket
        )

    Ticket.objects.bulk_create(tickets_to_create)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
