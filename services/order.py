from django.contrib.auth import get_user_model
from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = user.orders.create()
    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.pk).update(created_at=created_at)
        order.refresh_from_db()
    for ticket in tickets:
        movie_session = get_movie_session_by_id(ticket.get("movie_session"))
        order.tickets.create(
            movie_session=movie_session,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return user.orders.all()
    return Order.objects.all()
