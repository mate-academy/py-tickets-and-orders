from db.models import Order, Ticket, User
from django.db import transaction
from django.utils.dateparse import parse_datetime

@transaction.atomic
def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    created_at = parse_datetime(date) if date else None

    order = Order.objects.create(user=user)
    if created_at:
        order.created_at = created_at
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order

def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
