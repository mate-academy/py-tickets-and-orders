from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    # Get user
    user = get_user_model().objects.get(username=username)
    # Create Order
    order = Order(user=user)
    if date:
        order.date = date
    order.save()
    # Create tickets
    tickets_list = []
    for ticket in tickets:
        new_ticket = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )
        tickets_list.append(new_ticket)
    Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
