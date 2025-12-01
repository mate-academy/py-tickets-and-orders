from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        order.save()

        tickets_data = []
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            tickets_data.append(Ticket(order=order,
                                       row=ticket["row"],
                                       seat=ticket["seat"],
                                       movie_session=movie_session))
        Ticket.objects.bulk_create(tickets_data)


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
