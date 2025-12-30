from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None | str:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return f"User {username} does not exist"
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )


def get_orders(username: str = None) -> QuerySet | str:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            return f"User {username} does not exist"
    return Order.objects.all()
