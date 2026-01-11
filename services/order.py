from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username),
    )
    if date:
        order.created_at = date
    for ticket in tickets:
        order.tickets.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )
    order.save()
    return order


def get_orders(
        username: str = None,
) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
