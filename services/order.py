from typing import List, Dict, Optional
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession


def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    """
    Create an order with tickets in a transaction.
    """
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(id=ticket_data
                                                     ["movie_session"])
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order,
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    """
    Get all orders or filter by username.
    Returns a QuerySet for further operations.
    """
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
