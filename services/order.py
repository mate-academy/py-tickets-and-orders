from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        customer = None
        for user in User.objects.all():
            if user.username == username:
                customer = user
        order = Order.objects.create(user=customer)

        if date is not None:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(order=order,
                                  movie_session_id=ticket["movie_session"],
                                  row=ticket["row"],
                                  seat=ticket["seat"])


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-user")
