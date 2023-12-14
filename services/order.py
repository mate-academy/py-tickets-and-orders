from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: dict, username: str, date: datetime = None) -> None:
    try:
        order_data = {
            "user": username,
            "created_at": date}\
            if date else {"user": username}
        order = Order.objects.create(**order_data)
        for ticket_data in tickets:
            ticket_data["order"] = order
            Ticket.objects.create(**ticket_data)
    except Exception:
        transaction.set_rollback(True)
        raise ValueError


def get_orders(username: str = None) -> None:
    if username:
        return Order.objects.filter(username=username)
    return Order.objects.all()
