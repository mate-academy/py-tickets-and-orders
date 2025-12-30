from django.db import transaction
from db.models import Order, Ticket, User
from django.db.models import QuerySet
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str | None = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.refresh_from_db()

    for t in tickets:
        Ticket.objects.create(
            movie_session_id=t["movie_session"],
            order=order,
            row=t["row"],
            seat=t["seat"],
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
