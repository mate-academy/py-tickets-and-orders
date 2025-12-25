from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict[str: all]],
                 username: str,
                 date: str = None) -> Order:

    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise ValidationError(f"User '{username}' does not exist.")

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = created_at

        order.save()

        required_fields = {"row", "seat", "movie_session"}

        for ticket in tickets:
            if not required_fields.issubset(ticket):
                raise ValidationError("Missing required ticket fields")

            try:
                movie_session = MovieSession.objects.get(
                    pk=ticket["movie_session"])
            except MovieSession.DoesNotExist:
                raise ValidationError(f"Session with id: "
                                      f"{ticket['movie_session']} don't exist")

            Ticket.objects.create(
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=order)

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all().order_by("-id")

    if username:
        queryset = queryset.filter(user__username=username).order_by("-id")

    return queryset
