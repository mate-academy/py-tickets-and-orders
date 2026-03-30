

from django.db.models import QuerySet
from django.db import transaction
from datetime import datetime

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str,
                 date: datetime = None) -> list[Ticket]:
    try:
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
    except User.DoesNotExist:
        return []

    if date:
        order.created_at = date
        order.save()
    tickets_to_add = []

    movie_session_ids = [ticket["movie_session"] for ticket in tickets]
    sessions = {s.id: s for s in
                MovieSession.objects.filter(id__in=movie_session_ids)}

    for ticket in tickets:
        tickets_to_add.append(Ticket(
            order=order,
            movie_session=sessions[ticket["movie_session"]],
            row=ticket["row"],
            seat=ticket["seat"]
        ))
    return Ticket.objects.bulk_create(tickets_to_add)


def get_orders(username: str = None) -> QuerySet | None:
    try:
        if username:
            return Order.objects.filter(user=User.objects.get(
                username=username))
        else:
            return Order.objects.all()
    except User.DoesNotExist:
        return None
