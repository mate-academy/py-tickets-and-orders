from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket, User


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
        )


def get_orders(username: str = None, ) -> QuerySet:
    if username:
        return Order.objects.all().filter(user__username=username)
    return Order.objects.all()
