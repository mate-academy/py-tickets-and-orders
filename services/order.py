from django.db import transaction
from django.utils import timezone

from db.models import User, Order, MovieSession, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("User with the given username does not exist.")

    with transaction.atomic():
        if date:
            created_at = timezone.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            created_at = timezone.now()

        order = Order.objects.create(user=user)

        if date:
            Order.objects.filter(id=order.id).update(created_at=created_at)

        ticket_objects = []
        for ticket in tickets:
            movie_session_id = ticket.get("movie_session")
            try:
                movie_session = MovieSession.objects.get(id=movie_session_id)
            except MovieSession.DoesNotExist:
                raise ValueError(f"Movie session with ID"
                                 f" {movie_session_id} does not exist.")

            ticket_object = Ticket(
                order=order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            ticket_objects.append(ticket_object)

        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> list[Order] | Order:
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User with the given username does not exist.")
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
