from datetime import datetime

from typing import Optional

from django.contrib.auth import get_user_model

from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic()
def create_order(
    tickets: list[dict], username: str, date: Optional[str] = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
        )


def get_orders(username: Optional[str] = None) -> None:
    all_orders = Order.objects.all()
    if username:
        all_orders = all_orders.filter(user__username=username)
    return all_orders
