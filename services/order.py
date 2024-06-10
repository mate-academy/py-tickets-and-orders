from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, MovieSession, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session_id = ticket["movie_session"]
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )
    order.save()
    return order


def get_orders(username: str = None) -> Order:
    if username is not None:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
