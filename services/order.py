from typing import Optional

from django.db import transaction
from django.utils.timezone import now
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None) -> Order:
    order_date = date if date else now()
    user_instance = User.objects.get(username=username)
    order = Order.objects.create(user=user_instance, created_at=order_date)
    tickets_to_create = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order
        ) for ticket in tickets]
    Ticket.objects.bulk_create(tickets_to_create, batch_size=100)
    return order


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()
    if username:
        return orders.filter(user__username=username)
    return orders
