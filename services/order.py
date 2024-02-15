from typing import List, Dict
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: List[Dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]

            movie_session = MovieSession.objects.get(
                id=movie_session_id
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> List[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
