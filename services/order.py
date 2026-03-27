from typing import Optional, List
from django.db import transaction
from db.models import Order, Ticket, MovieSession, User
from django.db.models import QuerySet


def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user, _ = User.objects.get_or_create(username=username)

    with transaction.atomic():
        order = Order(user=user, created_at=date) if date else Order(user=user)
        order.save()

        ticket_objects = [
            Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: Optional[str]) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
