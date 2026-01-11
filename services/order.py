from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from db.models import Order, User, Ticket, MovieSession
from datetime import datetime
from django.db.models import QuerySet

def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(f"Date string '{date}' is not in the expected format '%Y-%m-%d %H:%M'.")
    if date is None:
        date = timezone.now()

    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"User with username {username} does not exist.")

        order = Order.objects.create(
            created_at=date,
            user=user)

        for ticket in tickets:
            try:
                movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            except MovieSession.DoesNotExist:
                raise ObjectDoesNotExist(f"MovieSession with id {ticket['movie_session']} does not exist.")

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            raise ValueError(f"User with username '{username}' does not exist.")
    return Order.objects.all()
