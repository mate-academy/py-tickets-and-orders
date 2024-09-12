from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(tickets: list[dict[str]],
                 username: str,
                 date: str = None) -> list[Ticket]:
    with transaction.atomic():
        created_tickets = []
        user, _ = User.objects.get_or_create(username=username)
        order = Order.objects.create(
            user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()
        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session")

            if (row is not None) and (
                    seat is not None) and (
                    movie_session_id is not None):
                created_ticket = Ticket.objects.create(
                    movie_session_id=movie_session_id,
                    order=order,
                    row=row,
                    seat=seat
                )
                created_tickets.append(created_ticket)
        return created_tickets


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
