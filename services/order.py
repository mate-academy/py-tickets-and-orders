from sqlite3 import DatabaseError
from typing import List, Dict, Any

from django.db import transaction

from db.models import Order, Ticket, User
from datetime import datetime


def create_order(tickets: Ticket, username: User, date: str) -> str:
    with transaction.atomic():
        try:
            order = Order.objects.create(user=username)

            if date:
                order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

            for ticket in tickets:
                ticket_order = Ticket.objects.create(
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=ticket["movie_session"])
                ticket_order.save()
            order.save()

        except DatabaseError:
            raise DatabaseError("Failed to create order")


def get_orders(username: User) -> List[Dict[str, Any]]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user=username)

    return orders
