
from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:

    try:
        user = get_user_model().objects.get(username=username)
    except ValueError:
        raise ValueError(f"user with username '{username}' does not exist")

    order = Order.objects.create(user=user)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.pk).update(created_at=created_at)
        order.created_at = created_at

    for ticket_data in tickets:
        if "movie_session" not in ticket_data:
            response = "each ticket dict must contain 'movie_session' key"
            raise ValueError(response)

        data = dict(ticket_data)
        ms = data.pop("movie_session")

        if isinstance(ms, (int, str)) and str(ms).isdigit():
            data["movie_session_id"] = int(ms)
        else:
            data["movie_session"] = ms

        Ticket.objects.create(order=order, **data)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
