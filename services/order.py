from django.db import transaction
from datetime import datetime
from db.models import Order, Ticket, User
from db.models import MovieSession


def create_order(tickets: list, username: str, date: str = None) -> User:
    user = User.objects.get(username=username)

    order_date = datetime.fromisoformat(date) if date else datetime.now()

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=order_date)

        for ticket_data in tickets:
            movie_session_id = ticket_data.pop("movie_session")
            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                **ticket_data
            )

    return order


def get_orders(username: str = None) -> User:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
