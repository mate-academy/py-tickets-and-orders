from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id
from services.user import get_user_by_username


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_by_username(username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    [
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=get_movie_session_by_id(ticket["movie_session"]),
            order=order
        )
        for ticket in tickets
    ]

    order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return get_user_by_username(username).orders.all()
    return Order.objects.all()
