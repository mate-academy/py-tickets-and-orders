from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> QuerySet:

    with transaction.atomic():

        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        tickets_instances = []
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )
            hall = movie_session.cinema_hall
            seats = hall.seats_in_row
            rows = hall.rows

            if ticket["seat"] > seats or ticket["row"] > rows:
                raise ValueError("Seat or row number exceeds limit.")
            tickets_instances.append(
                Ticket(movie_session_id=ticket["movie_session"],
                       order=order,
                       row=ticket["row"],
                       seat=ticket["seat"])
            )
        Ticket.objects.bulk_create(tickets_instances)
        return Ticket.objects.all()


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
