from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: list[dict], username, date=None):
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-user__username")
