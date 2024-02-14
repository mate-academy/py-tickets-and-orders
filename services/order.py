from typing import List, Dict
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: List[Dict], username: str, date: str = None) -> None:
    try:
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

                try:
                    movie_session = MovieSession.objects.get(
                        id=movie_session_id
                    )
                except MovieSession.DoesNotExist:
                    raise Exception("MovieSession does not exist.")

                Ticket.objects.create(
                    movie_session=movie_session,
                    order=order,
                    row=row,
                    seat=seat
                )

    except Exception as e:
        print(f"Error creating order: {e}")
        raise


def get_orders(username: str = None) -> List[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
