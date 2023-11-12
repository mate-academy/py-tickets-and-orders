from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = None
    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )
    for ticket in tickets:
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order_id=order.id
        ).save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    query_set = Order.objects.all()

    if username:
        query_set = query_set.filter(user__username=username)

    return query_set
