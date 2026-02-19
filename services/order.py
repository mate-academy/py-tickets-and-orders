from django.db.models import QuerySet

from db.models import User
from django.db import transaction
from datetime import datetime
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order_data = {"user": user}

    if date:
        order_data["created_at"] = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        pass

    order = Order.objects.create(**order_data)

    for ticket_data in tickets:
        movie_session_id = int(ticket_data["movie_session"])
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order, Order]:
    queryset = Order.objects.all()
    if username:
        try:
            queryset = queryset.filter(user__username=username)
        except User.DoesNotExist:
            pass

    queryset = queryset.select_related("user").prefetch_related(
        "tickets__movie_session__movie",
        "tickets__movie_session__cinema_hall"
    )
    return queryset
