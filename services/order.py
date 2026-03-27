from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict], username: str, date: str = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
            )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all().order_by("-user")
    if username:
        orders = orders.filter(user__username__icontains=username)

    return orders
