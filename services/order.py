from db.models import Order, User, Ticket


def create_order(
    tickets: list[Ticket], username: str, date: str
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username), date=date
    )
    for ticket in tickets:
        order.tickets.add(ticket)
    return order
