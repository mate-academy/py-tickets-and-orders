import datetime

from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets: dict, username, date=None):
    with transaction.atomic():
        if date:
            order_ = Order.objects.create(
                created_at=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M"),
                user=User.objects.get(username=username)
            )
        else:
            order_ = Order.objects.create(
                user=User.objects.get(username=username)
            )
        [
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                order=order_,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"])
            ) for ticket in tickets
        ]


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
