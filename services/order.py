from typing import List, Optional
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from datetime import datetime


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset: QuerySet[Order] = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=created_at)
        order.refresh_from_db()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order
