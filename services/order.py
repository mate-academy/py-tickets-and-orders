from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order_data = {"user": user}

    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        field = Order._meta.get_field("created_at")
        field.auto_now_add = False

        try:
            order_data["created_at"] = parsed_date
            order = Order.objects.create(**order_data)
        finally:
            field.auto_now_add = True
    else:
        order = Order.objects.create(**order_data)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(
            user=get_user_model().objects.get(username=username)
        )

    return orders
