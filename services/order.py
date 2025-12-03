from django.db import transaction
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime

from db.models import User, Order, Ticket, MovieSession


def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str = None
) -> None:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"User with username {username} does not exist")

        order = Order.objects.create(user=user)

        if date:
            parsed_date = parse_datetime(date)
            order.created_at = parsed_date
            order.save(update_fields=['created_at'])

        for ticket_data in tickets:
            try:
                movie_session = MovieSession.objects.get(id=ticket_data['movie_session'])
            except MovieSession.DoesNotExist:
                raise ObjectDoesNotExist(
                    f"MovieSession with id {ticket_data['movie_session']} does not exist"
                )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data['row'],
                seat=ticket_data['seat']
            )


def get_orders(username: str = None) -> QuerySet:
    from db.models import Order

    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
