from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user_id = get_user_model().objects.only("id").get(username=username).id
    order = Order.objects.create(user_id=user_id)
    if date is not None:
        order.created_at = date
    order.save()

    for ticket in tickets:
        movie_session = ticket.get("movie_session")

        Ticket.objects.create(
            movie_session_id=movie_session, order=order,
            row=ticket.get("row"), seat=ticket.get("seat")
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)

    return orders
