from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from services.user import get_user_by_username


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> Order:
    user = get_user_by_username(username)
    order = Order.objects.create(user=user)

    if date:
        from datetime import datetime
        order.created_at = datetime.fromisoformat(date)
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
