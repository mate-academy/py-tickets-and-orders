from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from services.user import get_user


@transaction.atomic
def create_order(
    tickets: list, username: str, date: str | None = None
) -> Order:
    user_order = get_user(username=username)

    new_order = Order.objects.create(user=user_order)
    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            row=ticket["row"],
            seat=ticket["seat"],
            order=new_order,
        )

    return new_order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        user_orders = get_user(username=username)
        return Order.objects.filter(user=user_orders)

    return Order.objects.all()
