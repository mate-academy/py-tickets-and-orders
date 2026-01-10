from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from db.models import User, Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order_data = {"user": user}
        if date:
            parsed_date = parse_datetime(date)
            if not parsed_date:
                raise ValueError("Nieprawidłowy format daty."
                                 " Użyj YYYY-MM-DD HH:MM:SS")
            order_data["created_at"] = parsed_date

        order = Order.objects.create(**order_data)
        ticket_objects = []
        for ticket_info in tickets:
            movie_session_id = ticket_info["movie_session"]
            movie_session = MovieSession.objects.get(id=movie_session_id)
            ticket = Ticket(
                order=order,
                movie_session=movie_session,
                row=ticket_info["row"],
                seat=ticket_info["seat"]
            )
            ticket_objects.append(ticket)
        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all().order_by("-created_at")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
