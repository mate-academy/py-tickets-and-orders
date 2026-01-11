from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None
                 ) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        date_in_datetime_format = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = date_in_datetime_format
        order.save()
    for ticket in tickets:
        order.tickets.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
