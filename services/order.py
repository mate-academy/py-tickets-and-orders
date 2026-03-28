from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import make_aware, make_naive
from datetime import datetime
from db.models import Order, Ticket  # Assuming Order and Ticket models exist
from typing import List, Dict, Optional
from django.db.models import QuerySet

# Get the correct User model (handles custom user models automatically)
User = get_user_model()


def create_order(
    tickets: List[Dict[str, int]], username: str, date: Optional[str] = None
) -> Order:
    """Create a new order with the given tickets and user."""
    user = get_user_model().objects.get(username=username)

    # ✅ Make datetime naive for SQLite if necessary
    created_at = (
        make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))
        if date
        else make_aware(datetime.now())
    )

    if not settings.USE_TZ:
        created_at = make_naive(created_at)  # SQLite does not support TZ-aware

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)

        tickets_to_create = [
            Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(tickets_to_create)

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    """Retrieve orders sorted by creation time (latest first)."""
    orders = Order.objects.select_related("user").order_by("-created_at")

    if username:
        orders = orders.filter(user__username=username)

    return orders
