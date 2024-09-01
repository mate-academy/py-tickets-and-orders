from django.db import transaction
from db.models import Order, Ticket
from db.models import User


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    new_data = {}
    if date:
        new_data["created_at"] = date
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)
        Order.objects.filter(id=order.id).update(**new_data)
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )
    return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
