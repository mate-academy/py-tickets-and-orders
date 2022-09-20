from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets, username, date=None):
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username=None):
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username).order_by("-created_at")
    return orders
