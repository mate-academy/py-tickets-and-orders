from django.db import transaction
from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str | datetime = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date is not None:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )

            Ticket.objects.create(order=order,
                                  row=ticket_data["row"],
                                  seat=ticket_data["seat"],
                                  movie_session=movie_session)

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if not username:
        return Order.objects.all()
    else:
        return Order.objects.filter(user__username=username)
