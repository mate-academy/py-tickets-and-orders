from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: list[dict], username: str, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)

        if date:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            created_at = None

        order = Order.objects.create(user=user, created_at=created_at)

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]

            ticket = Ticket(row=row, seat=seat, movie_session_id=movie_session_id, order=order)
            ticket.full_clean()
            ticket.save()


def get_orders(username: str = None):
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    orders = Order.objects.all()
    return orders
