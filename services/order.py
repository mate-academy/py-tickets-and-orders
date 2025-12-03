from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    new_order = Order(
        user=user
    )
    new_order.save()

    if date:
        new_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=new_order.pk).update(created_at=new_date)
        new_order.refresh_from_db()

    for ticket in tickets:
        new_ticket = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=new_order
        )
        new_ticket.save()

    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(
            user=user
        )
    return orders
