from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from db.models import Order, Ticket, MovieSession, User


def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(
            f"User with username {username} does not exist."
        )

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            created_at=date if date else timezone.now()
        )

        # Create tickets associated with the order
        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session")

            try:
                movie_session = MovieSession.objects.get(id=movie_session_id)
            except ObjectDoesNotExist:
                raise ValueError(
                    f"Movie session with id {movie_session_id} does not exist."
                )

            Ticket.objects.create(
                row=row,
                seat=seat,
                movie_session=movie_session,
                order=order
            )

    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user).order_by("-created_at")
        except ObjectDoesNotExist:
            return []
    return Order.objects.all().order_by("-created_at")
