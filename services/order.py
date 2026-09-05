from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(
        user=user,
        created_at=date
    )

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
