from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
        order.created_at = date

    ticket_objs = []
    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        if not all([movie_session_id, row, seat]):
            raise ValueError("Missing ticket data")

        movie_session = MovieSession.objects.get(id=movie_session_id)

        ticket_objs.append(
            Ticket(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            )
        )

    Ticket.objects.bulk_create(ticket_objs)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
