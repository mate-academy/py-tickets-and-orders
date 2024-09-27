from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist")
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username is not None:
        return Order.objects.filter(user__username=username)
    if username is None:
        return Order.objects.all()
