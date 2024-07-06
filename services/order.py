from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user = User.objects.get(username=username)

    with (transaction.atomic()):
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

    return order


def get_orders(username: str = None) -> list[dict]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
