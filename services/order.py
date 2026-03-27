from datetime import datetime
from db.models import User, Order, Ticket
from django.db import transaction


def create_order(tickets, username, date=None):
    user = User.objects.filter(username=username).first()
    if not user:
        raise ValueError("User not found")
    
    created_at = datetime.strptime(date, "%Y-%m-%d %H:%M") if date else datetime.now()
    
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)
        for ticket_data in tickets:
            Ticket.objects.create(order=order, **ticket_data)
    return order

def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()