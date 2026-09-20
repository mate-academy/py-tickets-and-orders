from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import MovieSession, Order, Ticket, User


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
) -> Order:
    user = User.objects.get(username=username)
    order_kwargs = {"user": user}
    if date:
        try:
            order_kwargs["created_at"] = datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            try:
                order_kwargs["created_at"] = datetime.strptime(
                    date, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                pass
    order = Order.objects.create(**order_kwargs)
    ticket_objects = [
        Ticket(
            order=order,
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            ),
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        for ticket_data in tickets
    ]
    for ticket in ticket_objects:
        ticket.full_clean()
    Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
