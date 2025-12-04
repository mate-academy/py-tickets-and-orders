from django.db import transaction
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str = None
) -> None:
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise ObjectDoesNotExist(
            f"User with username {username} does not exist"
        )

    order_data = {"user": user}
    if date:
        parsed_date = parse_datetime(date)
        order_data["created_at"] = parsed_date

    order = Order.objects.create(**order_data)

    for ticket_data in tickets:
        try:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
        except MovieSession.DoesNotExist:
            raise ObjectDoesNotExist(
                f'MovieSession with id {ticket_data["movie_session"]} '
                f"does not exist"
            )

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    from db.models import Order

    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
