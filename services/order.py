from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(id=order.id).update(created_at=date)

    ticket_list = []
    for ticket in tickets:
        new_ticket = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )
        new_ticket.full_clean()
        ticket_list.append(new_ticket)
    Ticket.objects.bulk_create(ticket_list)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
