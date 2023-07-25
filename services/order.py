from django.db.models import QuerySet
from django.db import transaction
from db.models import Ticket, Order, User


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
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


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
