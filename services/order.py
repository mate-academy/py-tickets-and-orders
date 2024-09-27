from typing import Optional

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic()
def create_order(
        tickets: Optional[list[dict]],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)
    if date:
        new_order.created_at = date
        new_order.save()
    for ticket in tickets:
        session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> Optional[list[str]]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
