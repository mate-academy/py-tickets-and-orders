from datetime import datetime
from typing import List
from django.db import transaction
from typing import Optional

from db.models import Order, MovieSession, User, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        if User.objects.filter(username=username):

            new_order = Order.objects.create(
                user=User.objects.get(username=username)
            )
            if date:
                date_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
                new_order.created_at = date_time
                new_order.save()

            for ticket in tickets:
                Ticket.objects.create(
                    order=new_order,
                    seat=ticket["seat"],
                    row=ticket["row"],
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"]
                    )
                )

            return new_order


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
