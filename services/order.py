from datetime import datetime
from django.db import transaction
from db.models import Order, User, Ticket
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:

    user = User.objects.get(username=username)
    order = Order.objects.create(user=user,)

    if date:
        order.created_at = date

    order.save()

    for ticket in tickets:
        row, seat, movie_session = (
            ticket["row"], ticket["seat"], ticket["movie_session"])
        Ticket.objects.create(
            order=order,
            row=row,
            seat=seat,
            movie_session_id=movie_session
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
