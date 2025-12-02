from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession

User = get_user_model()


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            created_ticket = Ticket(movie_session=movie_session,
                                    order=order,
                                    row=ticket["row"],
                                    seat=ticket["seat"],)
            created_ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user__username=username).order_by("-created_at")
    else:
        return Order.objects.all().order_by("-created_at")
