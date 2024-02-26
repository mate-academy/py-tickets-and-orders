from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()

    tickets_list = [
        Ticket(
            row=ticket_info["row"],
            seat=ticket_info["seat"],
            movie_session=get_movie_session_by_id(
                ticket_info["movie_session"]
            ),
            order=order
        )
        for ticket_info in tickets
    ]

    Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
