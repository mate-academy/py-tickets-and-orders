import datetime

from django.db import transaction

from db.models import Ticket, MovieSession, Order, User


def create_order(
        tickets: list[dict],
        username: str | None = None,
        date: datetime.datetime | None = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            Order.objects.filter(pk=order.pk).update(created_at=date)
            order.refresh_from_db()

        for ticket in tickets:
            movie_session_obj = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session_obj
            )


def get_orders(username: str | None = None) -> None:
    order_obj = Order.objects.all()
    if username:
        order_obj = order_obj.filter(user__username=username)
    return order_obj
