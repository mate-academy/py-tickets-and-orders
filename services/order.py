from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional
from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:

    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.created_at = date
        order.refresh_from_db()
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket_data["movie_session"]
        )
        ticket = Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session
        )
        ticket.save()
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
