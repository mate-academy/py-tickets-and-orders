from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=User.objects.get(
            username=username
        )
    )
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> Order:
    if username:
        return (Order.objects.select_related("user").
                filter(user__username=username))
    return Order.objects.all()
