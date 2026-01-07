from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket_data in tickets:
        movie_session = (
            MovieSession.objects.get(pk=ticket_data["movie_session"]))
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
