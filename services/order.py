from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from datetime import datetime

User = get_user_model()


@transaction.atomic
def create_order(tickets, username, date=None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username=None) -> models.QuerySet:
    qs = Order.objects.select_related("user").order_by("-created_at")
    if username:
        return qs.filter(user__username=username)
    return qs
