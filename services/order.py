from django.db import transaction

from db.models import Order, Ticket, User


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )
        order.save()


def get_orders(username: str = None) -> Order:
    order = Order.objects.all()
    if username:
        order = order.filter(user__username=username)

    return order
