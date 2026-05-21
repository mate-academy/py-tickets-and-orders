from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from services.user import get_user


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = get_user(username=username)

    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
        order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
