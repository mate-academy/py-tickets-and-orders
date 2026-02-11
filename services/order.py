from datetime import datetime

from django.db import transaction

from django.db.models import QuerySet

from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order | None:
    user_model = get_user_model()
    try:
        user = user_model.objects.get(username=username)
    except user_model.DoesNotExist:
        return None
    if date is not None:
        date1 = datetime.strptime(date, "%Y-%m-%d %H:%M")
        date1 = date1.replace(second=0, microsecond=0)
        order = Order.objects.create(user=user, created_at=date1)
    else:
        order = Order.objects.create(user=user)
    for ticket in tickets:
        Ticket.objects.create(order=order,
                              movie_session_id=ticket["movie_session"],
                              seat=ticket["seat"], row=ticket["row"])
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
