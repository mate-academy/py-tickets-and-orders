from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    tickets_list = []
    for ticket in tickets:
        tickets_list.append(Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        )

    for ticket in tickets_list:
        ticket.full_clean()

    Ticket.objects.bulk_create(tickets_list)

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
