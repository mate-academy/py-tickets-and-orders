from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()

@transaction.atomic
def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        pass
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket['movie_session'],
            order=order,
            row=ticket['row'],
            seat=ticket['seat']
        )
    return order

def get_orders(username=None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
