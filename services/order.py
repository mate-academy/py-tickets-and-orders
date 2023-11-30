from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            ),
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )


def get_orders(username: str = None) -> Order:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
