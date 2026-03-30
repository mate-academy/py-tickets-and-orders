import datetime

from django.db import transaction

from db.models import Order, Ticket, MovieSession, User


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | datetime.datetime | None = None,
) -> Order:
    user = User.objects.get(username=username)

    if date is not None:
        if isinstance(date, str):
            created_at = datetime.datetime.fromisoformat(date)
        else:
            created_at = date
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str | None = None):
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
