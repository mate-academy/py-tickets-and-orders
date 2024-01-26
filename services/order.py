from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_info in tickets:
            movie_session = (
                MovieSession.objects.get(id=ticket_info["movie_session"])
            )
            ticket = Ticket(
                row=ticket_info["row"],
                seat=ticket_info["seat"],
                movie_session=movie_session,
                order=order
            )
            ticket.save()
    return order


def get_orders(username: str = None) -> Order:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
