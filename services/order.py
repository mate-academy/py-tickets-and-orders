from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order
from datetime import datetime
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    usermodel = get_user_model()
    user = usermodel.objects.get(username=username)
    new_order = Order.objects.create(
        user=user,
    )
    if date:
        Order.objects.filter(pk=new_order.pk).update(created_at=date)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=new_order,
        )
    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
