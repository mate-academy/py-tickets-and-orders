from django.db.models import QuerySet
from db.models import Order, MovieSession, Ticket
from datetime import datetime
from django.db import transaction
from services import user


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None) -> None:
    if not tickets:
        return None

    current_user = user.get_user_model().objects.get(username=username)

    order = Order.objects.create(user=current_user)
    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        ticket = Ticket(
            order=order,
            movie_session=(MovieSession.
                           objects.
                           get(id=ticket_data["movie_session"])),
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket.full_clean()
        ticket.save()


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
