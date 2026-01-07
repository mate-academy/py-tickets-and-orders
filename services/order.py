from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        tickets_list = [
            Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets]

        Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    else:
        return Order.objects.all()
