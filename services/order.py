from typing import Optional, List, Dict, Any
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, MovieSession, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict[str, Any]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
        order.refresh_from_db()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
