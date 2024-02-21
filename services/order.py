from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:

    order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row, seat, movie_session_id = ticket.values()

        Ticket.objects.create(
            movie_session=MovieSession.objects.get(id=movie_session_id),
            order=order,
            row=row,
            seat=seat
        )
    return order


def get_orders(username: str = None) -> QuerySet:

    if username:
        order = Order.objects.filter(user__username=username)
    else:
        order = Order.objects.all()

    return order
