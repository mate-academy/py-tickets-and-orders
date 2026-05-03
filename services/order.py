from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None
                 ) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=parsed_date)
        order.refresh_from_db()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"]
                              )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
