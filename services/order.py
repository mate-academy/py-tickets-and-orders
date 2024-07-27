from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: User,
        date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(
                pk=ticket["movie_session"]
            ),
            order=order
        )


def get_orders(username: User = None) -> list[Ticket]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
