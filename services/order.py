from django.db import transaction
from db.models import Order, Ticket, MovieSession, User


@transaction.atomic
def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(pk=ticket_data['movie_session'])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data['row'],
            seat=ticket_data['seat']
        )

    return order


def get_orders(username=None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
