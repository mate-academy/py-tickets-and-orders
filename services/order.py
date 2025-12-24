from typing import Dict

from django.db import transaction
from db.models import User, Order, Ticket
from django.core.exceptions import ObjectDoesNotExist

def create_order(tickets: list[dict], username: str, date: str = None) -> Order | Dict:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return {"error": f"User with username {username} does not exist."}
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
    return order

def get_orders(username: str = None):
    try:
        if username:
            user = User.objects.get(username=username)  # This will raise an exception if the username doesn't exist
            return Order.objects.filter(user=user)
        return Order.objects.all()
    except ObjectDoesNotExist:
        return {"error": "User with the provided username does not exist."}
