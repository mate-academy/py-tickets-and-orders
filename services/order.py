from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str | None = None) -> Order:
    User = get_user_model()
    user = User.objects.get(username=username)

    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str | None = None)-> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username).order_by("-created_at")
    return Order.objects.all()
