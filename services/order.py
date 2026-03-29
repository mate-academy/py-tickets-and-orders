from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order


def create_order(tickets: list,
                 username: str,
                 date: Optional[datetime | str] = None) -> Order:
    from db.models import Order, Ticket, User
    try:
        if date:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M")

        with transaction.atomic():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise Exception("User does not exist")

            order = Order.objects.create(user=user)

            for ticket_data in tickets:
                Ticket.objects.create(
                    order=order,
                    movie_session_id=ticket_data["movie_session"],
                    row=ticket_data["row"],
                    seat=ticket_data["seat"]
                )

            if date:
                order.created_at = date
                order.save()

            return order
    except Exception as e:
        raise e


def get_orders(username: Optional[str] = None) -> QuerySet:
    from db.models import Order
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders
