from django.db.models import QuerySet
from django.db import transaction
from django.utils import timezone
from db.models import Order, Ticket, User


def create_order(
    username: str = None,
    user_id: int = None,
    tickets: list[dict] = None,
    date=None,
) -> Order:
    if username:
        user = User.objects.get(username=username)
    elif user_id:
        user = User.objects.get(id=user_id)
    else:
        raise ValueError("Either username or user_id must be provided")

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            created_at=date if date else timezone.now(),
        )

        if tickets:
            for t in tickets:
                Ticket.objects.create(
                    order=order,
                    movie_session_id=t.get("movie_session_id") or t.get("movie_session"),
                    row=t["row"],
                    seat=t["seat"],
                )

    return order


def get_orders(username: str = None) -> QuerySet:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
