from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from typing import List, Dict, Any

User = get_user_model()


@transaction.atomic
def create_order(tickets: List[Dict[str, Any]], username: str, date: Any = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User {username} does not exist.")

    created_at = date if date else timezone.now()
    order = Order.objects.create(user=user, created_at=created_at)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.save()
    return order


def get_orders(username: Optional[str] = None) -> List[Order]:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
