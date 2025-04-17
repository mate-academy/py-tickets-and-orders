from db.models import Order, Ticket, User, MovieSession
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username: {username} does not exists!")

    order_data = {"user": user}
    if date:
        parsed_date = parse_datetime(date)
        if not parsed_date:
            raise ValueError("")
        order_data["created_at"] = parsed_date

    order = Order.objects.create(**order_data)

    for ticket in tickets:
        Ticket.objects.create(
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]
            order=order
        )
    
    return order

def get_orders(username: str = None):
    if username:
        return Order.objects.get(user__username=username)
    else:
        return Order.objects.all()
