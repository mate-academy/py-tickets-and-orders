from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from datetime import datetime

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | None = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order(user=user)
    order.save()
    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for tt in tickets:
        ticket = Ticket(
            row=tt["row"],
            seat=tt["seat"],
            movie_session_id=tt["movie_session"],
            order=order
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
