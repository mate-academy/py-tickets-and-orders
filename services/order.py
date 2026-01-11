from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:

    user = get_user_model().objects.get(username=username)

    if date is not None:
        created_at = timezone.datetime.strptime(date, "%Y-%m-%d %H:%M")

    else:
        created_at = timezone.now()

    order = Order.objects.create(
        user=user
    )
    order.created_at = created_at

    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
