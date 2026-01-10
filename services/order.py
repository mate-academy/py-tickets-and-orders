# db/services/order.py
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket
from datetime import datetime
from typing import Optional


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    
    order_data = {"user": user}
    if date:
        order_data["created_at"] = datetime.strptime(date, "%Y-%m-%d %H:%M")
    
    order = Order.objects.create(**order_data)
    
    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
