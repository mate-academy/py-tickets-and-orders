from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
):
    new_order = Order(
        user=get_user_model().objects.get(
            username=username
        )
    )

    if date:
        new_order.created_at = date
        new_order.save()

    for elem in tickets:
        row, seat, movie_session = elem.values()
        Ticket(
            movie_session=get_movie_session_by_id(movie_session),
            order=new_order,
            row=row,
            seat=seat
        )


def get_orders(username: str = None):
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
