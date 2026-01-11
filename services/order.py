from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:  # Повертаємо саме Order, а не QuerySet
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)  # Створили без created_at

        if date is not None:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()  # Зберегли дату

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session,
                order=order,
            )

        return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
