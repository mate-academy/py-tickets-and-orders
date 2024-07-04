from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list,
        username: User,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            ticket = Ticket(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )
            ticket.full_clean()
            ticket.save()

        return order


def get_orders(username: User = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
