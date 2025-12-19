from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession

from datetime import datetime

User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None,
) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise ValueError(f"User {username} not found") from e

        # Create order first
        order = Order.objects.create(user=user)

        # Handle date if provided
        if date:
            try:
                # Parse the date format "2020-11-10 14:40"
                parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
                order.created_at = parsed_date
                order.save()
            except ValueError:
                try:
                    # Try ISO format as fallback
                    parsed_date = datetime.fromisoformat(date)
                    order.created_at = parsed_date
                    order.save()
                except ValueError:
                    raise ValueError(f"Invalid date format: {date}")

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            ms_id = ticket["movie_session"]

            try:
                movie_session = MovieSession.objects.get(id=ms_id)
                Ticket.objects.create(
                    row=row,
                    seat=seat,
                    movie_session=movie_session,
                    order=order,
                )
            except MovieSession.DoesNotExist as e:
                raise ValueError(f"MovieSession {ms_id} not found") from e

        return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.select_related("user").prefetch_related("tickets")
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
