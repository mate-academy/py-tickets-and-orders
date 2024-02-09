from django.db import transaction

from db.models import Order, Ticket, User


def create_order(
        tickets: [dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date

        for ticket in tickets:
            ticket_sample = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            ticket_sample.save()

        order.save()


def get_orders(username: str = None) -> [Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
