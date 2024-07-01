from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None
                 ) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session_id = ticket.get("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)
        ticket_seat = ticket.get("seat")
        ticket_row = ticket.get("row")
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            seat=ticket_seat,
            row=ticket_row)
    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
