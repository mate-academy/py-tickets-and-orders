from db.models import Order, Ticket, User, MovieSession
from datetime import datetime
from django.db import transaction


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                )
            )

        return order


def get_orders(username: str = None) -> Order:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders
