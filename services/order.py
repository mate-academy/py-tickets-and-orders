from datetime import datetime

from django.db import transaction
from django.db.models.query import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> Ticket:
    with transaction.atomic():
        my_order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            my_order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            my_order.save()
        return Ticket.objects.bulk_create(
            [
                Ticket(
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"]
                    ),
                    order=my_order,
                    row=ticket["row"],
                    seat=ticket["seat"]
                ) for ticket in tickets
            ]
        )


def get_orders(username: str = None) -> QuerySet:
    orders_to_get = Order.objects.all()
    if username:
        # return User.objects.get(username=username).orders.all()
        orders_to_get = orders_to_get.filter(user__username=username)
    return orders_to_get
