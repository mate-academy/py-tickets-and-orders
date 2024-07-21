from db.models import Order, Ticket
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(username=username)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"], seat=ticket["seat"],
                movie_session=ticket["movie_session"]
            )

        order.save()
    return order


def get_orders(username: str) -> list[dict]:
    if username:
        Order.objects.filter(username=username)
    return Order.objects.all()
