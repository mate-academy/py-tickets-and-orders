from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    tickets_objs = []
    for data in tickets:
        try:
            ticket = Ticket(
                order=order,
                row=data["row"],
                seat=data["seat"],
                movie_session_id=data["movie_session"]
            )
            ticket.full_clean()
            tickets_objs.append(ticket)
        except ValidationError as e:
            raise Exception(f"Invalid ticket data: {e}")

    Ticket.objects.bulk_create(tickets_objs)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
