from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order
from django.db.models import QuerySet
from datetime import datetime
from db.models import Ticket


User = get_user_model()

@transaction.atomic

def create_order(tickets: list, username: str, date: str | None = None) -> Order:
    user = get_user_model().objects.get(username=username)
    created_at = datetime.strptime(date, "%Y-%m-%d %H:%M") if date else datetime.now()
    order = Order.objects.create(user=user, created_at=created_at)

    ticket_objs = []
    for ticket in tickets:
        ticket_obj = Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session__id"],
        )
        ticket_objs.append(ticket_obj)

    Ticket.objects.bulk_create(ticket_objs)

    return order



def get_orders(username: str | None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset