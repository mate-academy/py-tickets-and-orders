from django.db import transaction
from django.contrib.auth import get_user_model


from db.models import Order, Ticket


User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    new_data = {}
    if date:
        new_data["created_at"] = date

    with transaction.atomic():
        order = Order.objects.create(
            user=user
        )
        Order.objects.filter(id=order.id).update(**new_data)

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
