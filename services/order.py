from datetime import datetime
from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession

@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None):
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=parsed_date)
    for t in tickets:
        Ticket.objects.create(
            movie_session_id=t["movie_session"],
            order=order,
            row=t["row"],
            seat=t["seat"]
        )

def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    qs = Order.objects.all().select_related("user").prefetch_related("tickets")
    if username:
        qs = qs.filter(user__username=username)
    return qs
