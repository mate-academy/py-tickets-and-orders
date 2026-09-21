from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: str | None = None,
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date is not None:
        order.created_at = date
        order.save()

    tickets_list = []
    for ticket_data in tickets:
        ticket = Ticket(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )

        ticket.full_clean()
        tickets_list.append(ticket)

    Ticket.objects.bulk_create(tickets_list)

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)

    return orders
