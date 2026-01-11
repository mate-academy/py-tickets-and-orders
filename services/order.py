from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None,
) -> Order | Exception:
    try:
        with transaction.atomic():
            user, _ = User.objects.get_or_create(username=username)
            order = Order.objects.create(user=user)

            if date:
                order.created_at = date
                order.save(update_fields=["created_at"])

            for ticket in tickets:
                movie_session, _ = MovieSession.objects.get_or_create(
                    id=ticket["movie_session"]
                )
                Ticket.objects.create(
                    movie_session=movie_session,
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"]
                )

        return order

    except Exception as e:
        print(f"Error occurred: {e}")
        raise e


def get_orders(username: str = None) -> QuerySet[Order]:

    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
