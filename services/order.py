from datetime import datetime
from django.db import transaction
from django.db.models import Q, QuerySet

from db.models import Order, Ticket
from services.user import find_users
from services.movie_session import get_movie_session_by_id


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> None:
    user = find_users(username=username).first()
    if not user:
        raise ValueError("User does not exist")
    if len(tickets) < 1:
        raise ValueError("Unable to create an order without any tickets")
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()
        for ticket in tickets:
            session = get_movie_session_by_id(ticket["movie_session"])
            if not session:
                raise ValueError("Movie session does not exist")
            Ticket.objects.create(
                order=order,
                movie_session=session,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    criteria = Q(user__username=username) if username else Q()
    return Order.objects.filter(criteria)
