from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user_id=user.id)
        if date:
            order.created_at = date
        for ticket in tickets:
            (Ticket
             .objects
             .create(movie_session=(MovieSession
                                    .objects
                                    .get(id=ticket["movie_session"])),
                     order=order,
                     row=ticket["row"],
                     seat=ticket["seat"]))
        order.save()


def get_orders(username: str = None) -> Order:
    order = Order.objects.order_by("-user")
    if username:
        order = order.filter(user__username=username)
    return order
