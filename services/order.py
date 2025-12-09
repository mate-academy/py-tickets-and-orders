from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession
from datetime import datetime

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str,
                 date: datetime | str | None = None) -> Order:
    user, _ = User.objects.get_or_create(username=username)

    try:
        if date:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)

        for ticket_data in tickets:
            session_id = ticket_data["movie_session"]
            row = ticket_data["row"]
            seat = ticket_data["seat"]

            movie_session = (MovieSession.objects.select_for_update()
                             .get(id=session_id))

            if Ticket.objects.filter(
                movie_session=movie_session,
                row=row,
                seat=seat
            ).exists():
                raise ValueError(
                    f"Seat ({row}, {seat}) is already booked "
                    f"for session {session_id}."
                )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            )

        return order

    except IntegrityError as e:
        raise ValueError(
            "A ticket in the order caused a unique "
            "constraint violation (seat already booked)."
        ) from e
    except MovieSession.DoesNotExist:
        raise ValueError(
            "One of the provided movie sessions does not exist."
        )


def get_orders(username: str | None = None) -> list[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            return Order.objects.none()
    else:
        return Order.objects.all()
