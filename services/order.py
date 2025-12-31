from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket


User = get_user_model()

@transaction.atomic
def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = parse_datetime(date)
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order

def get_orders(username=None):
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
