from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict], username: str = None, date: str = None
) -> None:
    user_model = get_user_model()

    user = (
        user_model.objects.get(username=username)
        if username
        else user_model.objects.first()
    )

    order_kwargs = {"user": user}
    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order_kwargs["created_at"] = parsed_date

    order = Order.objects.create(**order_kwargs)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
