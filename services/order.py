from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = date
    order.save()
    tickets_objects = []
    for ticket in tickets:
        ticket_instance = Ticket(order=order,
                                 row=ticket["row"],
                                 seat=ticket["seat"],
                                 movie_session_id=ticket["movie_session"])
        ticket_instance.clean()
        tickets_objects.append(ticket_instance)

    Ticket.objects.bulk_create(tickets_objects)


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
