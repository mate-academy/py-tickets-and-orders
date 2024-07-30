from django.db import transaction
from django.db.models.query import QuerySet

from services.movie_session import get_movie_session_by_id
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order_data = {"user": user}
    if date:
        order_data["created_at"] = date

    order = Order.objects.create(**order_data)
    order.save()

    for ticket_data in tickets:
        movie_session = get_movie_session_by_id(
            ticket_data["movie_session"]
        )
        ticket_create = Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket_create.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
