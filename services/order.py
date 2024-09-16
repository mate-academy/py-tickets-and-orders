from django.db import transaction
from django.db.models import QuerySet
from typing import List, Dict, Optional
from db.models import Order, Ticket, MovieSession
from services.user import User


@transaction.atomic
def create_order(
        tickets: List[Dict], username: str, date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
