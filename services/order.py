from db.models import Order, Ticket


def get_order(
        tickets: list[Order],
        username: str,
        date: str = None
) -> Order:
    order = Order.objects.create(user=username)
    if date:
        order.created_at = date
    for ticket in tickets:
        Ticket.objects.create(**ticket)