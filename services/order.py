import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, User


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
    print(order.created_at)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
