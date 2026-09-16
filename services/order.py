from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.refresh_from_db()
    tickets_to_create = []
    for ticket in tickets:
        ticket_object = Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )
        ticket_object.full_clean()
        tickets_to_create.append(ticket_object)
    Ticket.objects.bulk_create(tickets_to_create)
    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
