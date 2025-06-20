from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ObjectDoesNotExist


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    created_at = parse_datetime(date) if date else None

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if created_at:
            order.created_at = created_at
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Order.objects.none()
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
