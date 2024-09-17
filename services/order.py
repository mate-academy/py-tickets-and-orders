from django.db.models import QuerySet
from db.models import Order, Ticket, User
from django.db import transaction


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:

    user = User.objects.get(username=username)

    order = Order.objects.create(user_id=user.id)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row = ticket.get("row")
        seat = ticket.get("seat")
        movie_session = ticket.get("movie_session")

        Ticket.objects.create(
            movie_session_id=movie_session,
            row=row,
            seat=seat,
            order_id=order.id
        )


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return user.orders.all()
    return Order.objects.all()
