from __future__ import annotations

from datetime import datetime

from django.db.transaction import atomic

from db.models import Order, User, Ticket


@atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    user_ = User.objects.get(username=username)
    order = Order.objects.create(user=user_)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
    for ticket in tickets:
        if ticket:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order_id=order.id,
            )
    return order


def get_orders(username: str | None = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
