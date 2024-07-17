from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    tickets_for_bd = []
    for ticket in tickets:
        tmp_ticket = Ticket(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )
        tmp_ticket.full_clean()
        tickets_for_bd.append(tmp_ticket)
    Ticket.objects.bulk_create(tickets_for_bd)
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
