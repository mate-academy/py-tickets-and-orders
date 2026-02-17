from typing import List
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: str = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    session_ids = {ticket["movie_session"] for ticket in tickets}
    if len(session_ids) != 1:
        raise Exception("All tickets must belong to the same movie session")

    movie_session_id = session_ids.pop()
    session = MovieSession.objects.get(id=movie_session_id)

    new_tickets = [
        Ticket(
            movie_session=session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(new_tickets)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
