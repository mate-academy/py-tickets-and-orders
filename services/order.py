from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    if not tickets:
        raise ValueError()

    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date:
        new_order.created_at = date
        new_order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data.get("movie_session"),
            order=new_order,
            row=ticket_data.get("row"),
            seat=ticket_data.get("seat"),
        )
    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
