from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise ValidationError(f"User with name {username} does not exists")

    order = Order.objects.create(user=user)

    if date:
        try:
            date_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date_time
            order.save(update_fields=["created_at"])
        except ValueError:
            raise ValidationError(
                "wrong date format, should be YYYY-MM-DD HH:MM"
            )

    movie_sessions = MovieSession.objects.filter(
        id__in=[ticket["movie_session"]
                for ticket in tickets]
    )

    dict_movie_sessions = {session.id: session for session in movie_sessions}

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=dict_movie_sessions[ticket["movie_session"]],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    try:
        if username:
            user = get_user_model().objects.get(username=username)
            return Order.objects.filter(user=user)
    except get_user_model().DoesNotExist:
        raise ValidationError(
            f"User with username '{username}' does not exist"
        )
    return Order.objects.all()
