from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import User, Order, MovieSession, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get_or_create(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user[0])

        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> list[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
