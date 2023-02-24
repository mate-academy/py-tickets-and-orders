from __future__ import annotations

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    with transaction.atomic():
        user = get_object_or_404(get_user_model(), username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all().order_by("-user__username")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
