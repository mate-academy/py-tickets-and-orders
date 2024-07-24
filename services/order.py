from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            user.created_at = date
            user.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"], seat=ticket["seat"]
            )

        order.save()
    return order


def get_orders(username: str) -> None:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
