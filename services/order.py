from datetime import datetime
from typing import Optional, List, Dict

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = parsed_date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders_data = Order.objects.all()
    if username:
        orders_data = orders_data.filter(user__username__iexact=username)

    return orders_data
