from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession, User
from django.utils import timezone


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    if date:
        created_at = timezone.make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))

    else:
        created_at = timezone.now()

    order = Order.objects.create(user=user, created_at=created_at)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
