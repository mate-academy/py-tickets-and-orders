from db.models import Order
from django.db import transaction
from django.contrib.auth import get_user_model
import datetime


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(created_at=date, user_id=user.id)
    for ticket in tickets:
        row, seat, session = ticket.values()
        order.tickets.create(row=row, seat=seat, movie_session_id=session)
    if date:
        order.created_at = date
    order.save()
    return order


def get_orders(username: str = None) -> Order:
    order = Order.objects.all()
    if username:
        return order.filter(user__username=username)
    return order
