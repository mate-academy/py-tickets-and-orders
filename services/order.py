from __future__ import annotations

from typing import Dict, Iterable, Optional
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket


User = get_user_model()


def _parse_created_at(date: Optional[str]) -> Optional[datetime]:
    """Converte string em datetime; retorna None se vazio ou inválido."""
    if not date:
        return None
    dt = parse_datetime(date)
    if dt is not None:
        return dt
    # fallback "YYYY-MM-DD HH:MM"
    try:
        return datetime.strptime(date, "%Y-%m-%d %H:%M")
    except ValueError:
        return None


@transaction.atomic
def create_order(
    tickets: Iterable[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    """
    Cria um pedido e seus tickets de forma atômica.
    `tickets` deve ser uma sequência de dicts com chaves:
    - movie_session (int)
    - row (int)
    - seat (int)
    """
    user = User.objects.get(username=username)

    # 1) cria o Order (auto_now_add preencherá com 'now()')
    order = Order.objects.create(user=user)

    # 2) se foi passada uma data, sobrescreve após a criação
    created_at = _parse_created_at(date)
    if created_at is not None:
        # update() evita rodar auto_now_add novamente
        Order.objects.filter(pk=order.pk).update(created_at=created_at)
        order.refresh_from_db(fields=["created_at"])

    # 3) cria tickets, validando via save() -> full_clean()
    for ticket_data in tickets:
        ticket = Ticket(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.save()

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    """
    Retorna pedidos ordenados (veja Meta.ordering no modelo).
    Se `username` for informado, filtra por esse usuário.
    """
    qs = Order.objects.all()
    if username is not None:
        qs = qs.filter(user__username=username)
    return qs
