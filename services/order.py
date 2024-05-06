from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(created_at=date, user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            session = MovieSession.objects.get(pk=ticket["movie_session"])
            ticket = Ticket.objects.create(row=ticket["row"],
                                           seat=ticket["seat"],
                                           order=order,
                                           movie_session=session)
            ticket.save()


def get_orders(username: str = None) -> list[dict]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-created_at")
