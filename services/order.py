from django.db import transaction
from db.models import Order, Ticket, User


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
        return order


def get_orders(username: None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
