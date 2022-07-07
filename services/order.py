from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date=None
):
    with transaction.atomic():
        user_id = get_user_model().objects.get(username=username).id
        new_order = Order.objects.create(user_id=user_id)

        if date:
            new_order.created_at = date

        new_order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket["movie_session"])

            Ticket.objects.create(
                movie_session=movie_session,
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
