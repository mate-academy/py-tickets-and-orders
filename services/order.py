from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict], username: str, date: str | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order = Order.objects.get(user=user)
        order.created_at = date
        order.save()

    for ticket_info in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_info["movie_session"],
            order=order,
            row=ticket_info["row"],
            seat=ticket_info["seat"]
        )
    return order


def get_orders(username: str | None = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
