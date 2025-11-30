from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    ticket_objects = []
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket_data["movie_session"]
        )

        ticket = Ticket(
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            order_id=None  # Временно None
        )
        ticket_objects.append((ticket, movie_session))

    order = Order.objects.create(user=user)

    if date:
        order.created_at = parse_datetime(date)
        order.save()

    validated_tickets = []
    for ticket, movie_session in ticket_objects:
        ticket.order = order
        ticket.full_clean()
        validated_tickets.append(ticket)

    Ticket.objects.bulk_create(validated_tickets)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()

    user = get_user_model().objects.get(username=username)

    return user.orders.all()
