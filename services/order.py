from django.contrib.auth import get_user_model
from django.db import transaction


from db.models import Order, Ticket
from django.utils.dateparse import parse_datetime
User = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = parse_datetime(date)
        order.save(update_fields=["created_at"])

    for data in tickets:
        Ticket.objects.create(movie_session_id=data["movie_session"],
                              order=order,
                              row=data["row"],
                              seat=data["seat"])
    return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
