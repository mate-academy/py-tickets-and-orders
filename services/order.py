from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model


from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        current_order = Order.objects.create(user=user)

        if date:
            current_order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                order=current_order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )

        current_order.save()
        return current_order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
