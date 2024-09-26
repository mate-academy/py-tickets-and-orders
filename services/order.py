from typing import List, Optional

from django.db import transaction

from db.models import Order, User, MovieSession, Ticket


def create_order(tickets: List[dict],
                 username: str,
                 date: Optional[str] = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session_id = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session_id,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
