from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession


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
    tickets = [
        Ticket(
            movie_session=MovieSession.objects.get(
                id=info["movie_session"]
            ),
            order=order,
            row=info["row"],
            seat=info["seat"]
        )
        for info in tickets
    ]
    Ticket.objects.bulk_create(tickets)


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username).distinct()
    return orders
