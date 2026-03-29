import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    try:
        user = User.objects.get(username=username)

        if date:
            try:
                created_at = datetime.datetime.strptime(
                    date,
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                created_at = datetime.datetime.strptime(
                    date,
                    "%Y-%m-%d %H:%M"
                )
        else:
            created_at = datetime.datetime.now()

        order = Order.objects.create(user=user)
        order.created_at = created_at
        order.save(update_fields=["created_at"])
        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
        return order
    except Exception as e:
        raise e


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
