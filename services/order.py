from django.db import transaction

from db.models import Ticket, Order, User


def create_order(
    tickets: list[Ticket],
    username: str,
    date: str = None
):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session_id=ticket["movie_session"]
            )


def get_orders(username=None):
    queryset = Order.objects.all().order_by("-id")
    if username:
        queryset = queryset.filter(user__username__exact=username)
    return queryset
