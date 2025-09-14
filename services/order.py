from django.db import transaction
from db.models import Ticket, Order
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = parse_datetime(
            date).strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=get_movie_session_by_id(
                movie_session_id=ticket["movie_session"]
            ),
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.select_related("user").order_by("-created_at")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
