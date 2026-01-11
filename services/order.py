from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    new_tickets = []
    movie_session = MovieSession.objects.get(
        pk=tickets[0].get("movie_session")
    )
    for data in tickets:
        if data.get("movie_session") != movie_session.id:
            movie_session = MovieSession.objects.get(data.get("movie_session"))
        tick = Ticket(
            row=data.get("row"),
            seat=data.get("seat"),
            movie_session=movie_session,
            order=order
        )
        new_tickets.append(tick)
    new_tickets = Ticket.objects.bulk_create(new_tickets)
    order.tickets.set(new_tickets)
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
