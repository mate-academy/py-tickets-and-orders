from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> Order:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"])
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
