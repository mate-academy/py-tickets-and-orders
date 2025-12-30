from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from services.movie_session import get_movie_session_by_id


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
    created_tickets = [
        Ticket(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session=get_movie_session_by_id(ticket.get("movie_session")),
            order=order,
        ) for ticket in tickets
    ]
    Ticket.objects.bulk_create(created_tickets)


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        queryset = Order.objects.filter(user=user)
    return queryset
