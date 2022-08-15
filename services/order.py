from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model


def create_order(tickets: list[dict], username: str, date=None):
    with transaction.atomic():

        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

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


def get_orders(username=None):
    order = Order.objects.all().order_by("-id")
    if username:
        order = order.filter(user__username=username)

    return order
