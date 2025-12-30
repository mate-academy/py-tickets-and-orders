from typing import List, Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession, User

from datetime import datetime


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    for ticket_data in tickets:
        movie_session_id = ticket_data.pop("movie_session")
        movie_session = MovieSession.objects.get(pk=movie_session_id)
        ticket_data["movie_session"] = movie_session
        Ticket.objects.create(order=order, **ticket_data)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
