from db.models import Order, Ticket, User
from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    with transaction.atomic():
        get_my_user = User.objects.get(username=username)
        order = Order(user=get_my_user)
        order.save()
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )
    return order


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
