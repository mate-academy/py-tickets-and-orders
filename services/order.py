
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    # Знаходимо користувача за username
    try:
        user = get_user_model().objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError(
            f"User with username '{username}' does not exist"
        )

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            try:
                order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValidationError(
                    "Invalid date format. Use 'YYYY-MM-DD HH:MM'."
                )
        else:
            order.created_at = timezone.now()

        for ticket_data in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ValidationError(
                    f"Movie session with id "
                    f"{ticket_data['movie_session']} does not exist"
                )
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session
            )
        order.save()

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
