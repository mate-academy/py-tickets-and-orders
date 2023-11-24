from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.db.models.query import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        user_order = Order.objects.create(user=user)

        if date:
            user_order.created_at = date
            user_order.save()

        for ticket_data in tickets:
            movie_session_id = ticket_data.get("movie_session")
            movie_session = MovieSession.objects.get(id=movie_session_id)
            ticket_data["movie_session"] = movie_session
            Ticket.objects.create(order=user_order, **ticket_data)

    return user_order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
