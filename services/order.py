from django.db import transaction
from django.db.models import DateTimeField, QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: User.username,
        date: DateTimeField = None
) -> Order:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date:
        order.created_at = date
    (Ticket.objects.bulk_create(
        [Ticket(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order_id=order.id) for ticket in tickets]))
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet | Order:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
