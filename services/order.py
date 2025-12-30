from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    for item in tickets:
        movie_session = MovieSession.objects.get(id=item["movie_session"])
        Ticket.objects.create(movie_session=movie_session,
                              seat=item["seat"],
                              row=item["row"],
                              order=order,)
    order.save()
    return order


def get_orders(username: str = None) -> list[Order]:
    order = Order.objects.all()
    if username:
        order = order.filter(user__username__icontains=username)
    return order
