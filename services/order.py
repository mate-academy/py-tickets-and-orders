from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list,
                 username: str = None,
                 date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=(
                    MovieSession.objects
                    .get(id=ticket["movie_session"])
                ),
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
    # user = User.objects.get(username=username)
    # if date:
    #     created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    # with transaction.atomic():
    #     order = Order.objects.create(user=user, created_at=created_at)
    #     for ticket in tickets:
    #         Ticket.objects.create(order=order, row=ticket["row"], seat=ticket["seat"],
    #                               movie_session_id=ticket["movie_session"])
    # return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
