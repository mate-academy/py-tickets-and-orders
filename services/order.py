from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, MovieSession
from django.contrib.auth import get_user_model


User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():

        user = User.objects.get(username=username)
        if date:
            order = Order.objects.create(user=user)
            order.created_at = date
            order.save()
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            ticket_data = {
                "ticket_row": ticket["row"],
                "ticket_seat": ticket["seat"],
                "session_id": ticket["movie_session"]

            }
            movie = MovieSession.objects.get(id=ticket_data["session_id"])
            ticket = Ticket(movie_session=movie,
                            order=order,
                            row=ticket_data["ticket_row"],
                            seat=ticket_data["ticket_seat"])
            ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
