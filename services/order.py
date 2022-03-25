from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list,
                 username,
                 date=None,
                 ):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
