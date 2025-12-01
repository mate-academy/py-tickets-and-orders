from datetime import datetime

from django.db.models import QuerySet

from db.models import Ticket, Order

from django.db import transaction

from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.create_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])

    for ticket_dict in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_dict["movie_session"],
            seat=ticket_dict["seat"],
            row=ticket_dict["row"],
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
