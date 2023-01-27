from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username__exact=username)
        )

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> Order:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
