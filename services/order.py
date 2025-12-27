from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None
) -> Order:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(
        user=user,
    )
    if date:
        new_order.created_at = date
    new_order.save()

    for ticket in tickets:
        movie_session_instance = (get_movie_session_by_id
                                  (ticket["movie_session"]))
        new_ticket = Ticket.objects.create(
            movie_session=movie_session_instance,
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"])
        new_ticket.save()
    return new_order


def get_orders(
    username: str = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all().order_by("-created_at")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
