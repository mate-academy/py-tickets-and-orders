from db.models import MovieSession, Order, Ticket
from django.contrib.auth import get_user_model
from django.db import transaction


@transaction.atomic
def create_order(
    tickets: list[dict], username: str, date: str | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
        )


def get_orders(username: str | None = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
