from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from .movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
    for ticket in tickets:
        new_ticket = Ticket.objects.create(
            movie_session=get_movie_session_by_id(ticket["movie_session"]),
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
        new_ticket.save()
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
