from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, MovieSession, Ticket


@transaction.atomic
def create_order(tickets: str, username: str, date: str = None) -> None:
    user, created = get_user_model().objects.get_or_create(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session_id = ticket_data.get("movie_session")
        movie_session, _ = (MovieSession.objects.get_or_create(
            id=movie_session_id)
        )
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=row, seat=seat
        )
    return order


def get_orders(username: str = None) -> None:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
