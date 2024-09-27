from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date=None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.
                get(movie_id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> Order:
    """Getting all orders for the user with the provided username,
    else returns all orders"""
    if username:
        return Order.objects.filter(user__username=username).all()
    return Order.objects.all().order_by("-id")
