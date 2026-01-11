from db.models import Order, Ticket, User
from typing import Optional, Any
from django.utils import timezone
import datetime

from django.db import transaction


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[datetime.datetime] = None) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
            order = Order.objects.create(
                user=user,
                created_at=date or timezone.now(),
            )

            print(f"Creating order with date: {order.created_at}")

            for ticket in tickets:
                Ticket.objects.create(
                    movie_session_id=ticket["movie_session"],
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"]
                )

            return order
        except Exception as e:
            print(f"Error creating order: {e}")
            # Przy wystąpieniu wyjątku cała transakcja zostanie wycofana
            raise


def get_orders(username: Optional[str] = None) -> Any:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
