from typing import Optional
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


def create_ticket(ticket_data: dict, order: Order) -> Ticket:
    ticket = Ticket(
        row=ticket_data.get("row"),
        seat=ticket_data.get("seat"),
        movie_session=get_movie_session_by_id(
            ticket_data.get("movie_session")
        ),
        order=order,
    )
    ticket.full_clean()
    ticket.save()
    return ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            create_ticket(ticket_data, order)


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
