from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: str | None = None) -> Order:
    user = get_user_model().objects.get(username=username)
    created_at = None
    kwargs = {"user": user}

    if date is not None:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

    if created_at is not None:
        kwargs["created_at"] = created_at

    order = Order.objects.create(**kwargs)

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              order=order, row=ticket["row"],
                              seat=ticket["seat"])

    return order


def get_orders(username: None | str = None) -> QuerySet[Order]:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username).select_related("user")
    
    qs = qs.filter(user__username=username)

    return qs
