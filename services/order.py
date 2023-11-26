from db.models import Order, User, Ticket, MovieSession
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(
            user__username=username
        ).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
