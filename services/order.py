from django.db import transaction
from db.models import Order, Ticket

def create_order(tickets, username, date=None):
    with transaction.atomic():
        order = Order.objects.create(user=username, created_at=date)

        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session = ticket_data.get("movie_session")
            ticket = Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session=movie_session
            )

        return order


def get_orders(username=None):

    if username is not None:
        orders = Order.objects.filter(user=username)
    else:
        orders = Order.objects.all()

    return orders
