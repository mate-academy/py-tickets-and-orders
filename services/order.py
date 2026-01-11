from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id



def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        tickets_list = [
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=get_movie_session_by_id(ticket.get("movie_session")),
                order=order,
            ) for ticket in tickets
        ]
        Ticket.objects.bulk_create(tickets_list)

def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
