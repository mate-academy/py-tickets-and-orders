# db/services/order.py
from django.db import transaction
from db.models import Order, Ticket, User
from datetime import datetime


def create_order(tickets: list, username: str, date: str = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
        return order


def get_orders(username: str = None):
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
