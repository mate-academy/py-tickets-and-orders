from typing import List, Dict, Optional
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        # Atualiza diretamente no banco, sem chamar save()
        Order.objects.filter(id=order.id).update(
            created_at=datetime.fromisoformat(date))
        # Refresh para garantir que order.created_at reflita o valor atualizado
        order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
