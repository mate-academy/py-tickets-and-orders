from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    order_data = {"user": user}
    if date:
        order_data["created_at"] = date

    order = Order.objects.create(**order_data)
    tickets_to_create = []
    for item in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=item["movie_session"],
            row=item["row"],
            seat=item["seat"],
        )
        ticket.full_clean()
        tickets_to_create.append(ticket)
    Ticket.objects.bulk_create(tickets_to_create)


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
