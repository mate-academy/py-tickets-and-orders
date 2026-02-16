from django.db import transaction
from db.models import Order, Ticket, User
from django.db.models.query import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict], username: str, date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        ticket = Ticket(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet["Order"]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
