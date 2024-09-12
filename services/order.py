from django.contrib.auth import get_user_model

from db.models import Order, MovieSession, Ticket
from django.db import transaction


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date

    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session_id = ticket_data.get("movie_session")

        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=row,
            seat=seat
        )

    order.save()


@transaction.atomic
def get_orders(username: str = None) -> list[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()

    return orders
