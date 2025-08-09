from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional
from datetime import datetime

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    
    # Optional: Validate no duplicate seats in same session
    for ticket_data in tickets:
        existing_ticket = Ticket.objects.filter(
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        ).exists()
        if existing_ticket:
            raise ValueError(f"Seat {ticket_data['row']}-{ticket_data['seat']} already taken")
    
    order = Order.objects.create(user=user)
    
    if date:
        order.created_at = datetime.fromisoformat(date)
        order.save()
    
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session,
            order=order
        )
    
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()


def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)


def get_user_orders(user_id: int) -> QuerySet[Order]:
    return Order.objects.filter(user_id=user_id)
