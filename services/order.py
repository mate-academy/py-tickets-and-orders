from django.db import transaction, models
from django.contrib.auth import get_user_model
from typing import List, Dict, Optional
from datetime import datetime

from db.models import Order, Ticket, MovieSession

# Pega o modelo de usuário apenas uma vez
User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)  # Usa o modelo correto

    if date:
        # datetime naive para SQLite
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = datetime.now()

    order = Order.objects.create(user=user, created_at=created_at)

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


def get_orders(username: Optional[str] = None) -> models.QuerySet[Order]:
    qs = Order.objects.all().order_by("-created_at")
    if username:
        qs = qs.filter(user__username=username)
    return qs
