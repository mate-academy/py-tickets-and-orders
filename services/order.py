from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            ),
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: str | None = None) -> list[Order]:
    if username:
        return list(Order.objects.filter(user__username=username))
    return list(Order.objects.all())
