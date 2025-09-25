from django.db.models import QuerySet
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from db.models import Ticket, User, Order


@transaction.atomic
def create_order(tickets: int, username: str, date: list[str] = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist")

    order = Order.objects.create(
        user=user,
        created_at=date if date else timezone.now()
    )

    ticket_objects = []
    for ticket_data in tickets:
        ticket_objects.append(
            Ticket(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=ticket_data["movie_session"]
            )
        )

    Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: list[str] = None) -> QuerySet[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValueError(f"User with username "
                             f"'{username}' does not exist")
        return Order.objects.filter(user=user)
    return Order.objects.all()
