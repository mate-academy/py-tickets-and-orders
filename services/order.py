import datetime
from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket

User = get_user_model()


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime.datetime = None,
) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            ticket = Ticket(
                movie_session_id=ticket_data["movie_session"],
                order=new_order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
            ticket.save()

    return new_order


def get_orders(username: str = None) -> QuerySet[Order] | Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
