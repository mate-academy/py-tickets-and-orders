from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=new_order.id).update(created_at=date)
        new_order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=new_order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.select_related("user").all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
