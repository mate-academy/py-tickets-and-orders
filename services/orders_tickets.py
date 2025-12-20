from django.db.models import QuerySet
from db.models import Order, Ticket


def create_order(user_id: int) -> Order:
    return Order.objects.create(user_id=user_id)


def get_orders() -> QuerySet:
    return Order.objects.all()


def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)


def create_ticket(
    order_id: int, movie_session_id: int, row: int, seat: int
) -> Ticket:
    return Ticket.objects.create(
        order_id=order_id,
        movie_session_id=movie_session_id,
        row=row,
        seat=seat,
    )


def get_tickets(order_id: int) -> QuerySet:
    return Ticket.objects.filter(order_id=order_id)
