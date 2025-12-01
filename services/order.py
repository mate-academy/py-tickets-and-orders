from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Ticket, Order, MovieSession
# from tests.test_main import users_data


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        user_ = User.objects.get(username=username)
        order = Order(user=user_)
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(order=order, movie_session=movie_session,
                                  row=ticket["row"], seat=ticket["seat"])


# def get_orders(username: str = None) -> QuerySet:
#     orders = Order.objects.all()
#     if username:
#         orders = orders.filter(user__username=username)
#     return orders.order_by("created_at", "user__username")
def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders.order_by("created_at", "user__username")