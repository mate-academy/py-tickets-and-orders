from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession, User


def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(
                f"User with username '{username}' does not exist."
            )

        order = Order.objects.create(user=user)

        if date:
            Order.objects.filter(id=order.id).update(created_at=date)
            order.created_at = date

        for ticket_data in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ObjectDoesNotExist(
                    f"Movie session with id {ticket_data['movie_session']} "
                    f"does not exist."
                )

            Ticket.objects.create(movie_session=movie_session,
                                  order=order,
                                  row=ticket_data["row"],
                                  seat=ticket_data["seat"])

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
