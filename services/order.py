from datetime import datetime
from django.db import transaction
from django.db.models import Q, QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.filter(username=username).first()
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
