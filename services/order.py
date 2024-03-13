from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
        tickets: list[Ticket], username: str, date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        if date:
            # date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(created_at=date, user=user)
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

def get_orders(username: str = None) -> QuerySet:
    get_orders = Order.objects.all()
    if username:
        get_orders = Order.objects.filter(user__username=username)
    return get_orders
