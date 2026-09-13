from db.models import Order, Ticket
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    get_my_user = User.objects.get(username=username)
    order = Order.objects.create(user=get_my_user)
    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.refresh_from_db()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
