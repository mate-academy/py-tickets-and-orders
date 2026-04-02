from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"])
        return order


def get_orders(username: str = None) -> QuerySet:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
