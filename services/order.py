from db.models import Order, Ticket, User
from django.db import transaction


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str | None = None) -> None:

    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        session_id = ticket["movie_session"]
        ticket = Ticket.objects.create(row=ticket["row"],
                                       seat=ticket["seat"],
                                       order=order,
                                       movie_session_id=session_id)
        ticket.save()


def get_orders(username: str | None = None) -> list[dict]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-created_at")
