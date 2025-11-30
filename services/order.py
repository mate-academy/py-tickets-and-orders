from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    UserModel = get_user_model()
    user = UserModel.objects.get(username=username)
    created_at = parse_datetime(date) if date else None

    order = Order.objects.create(user=user)
    if created_at:
        order.created_at = created_at
        order.save()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    UserModel = get_user_model()
    if username:
        try:
            user = UserModel.objects.get(username=username)
            return Order.objects.filter(user=user)
        except UserModel.DoesNotExist:
            return Order.objects.none()
    else:
        return Order.objects.all()
