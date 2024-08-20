from django.db import transaction
from db.models import Order, Ticket, User
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    if not date:
        date = datetime.now()
    order = Order.objects.create(
        user=user,
        created_at=date
    )
    for ticket in tickets:
        ticket.order = order
        ticket.save()
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
