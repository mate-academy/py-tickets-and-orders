from datetime import datetime

from django.db import transaction

from db.models import Order, User, MovieSession

from db.models import Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order(user=user)
        order.save()
        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            Order.objects.filter(pk=order.pk).update(created_at=parsed_date)
            order.refresh_from_db()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )
            Ticket.objects.create(order=order,
                                  movie_session=movie_session,
                                  seat=ticket["seat"],
                                  row=ticket["row"])
    return order


def get_orders(username: str = None) -> list[Order]:
    orders = Order.objects.all()
    with transaction.atomic():
        if username:
            orders = orders.filter(user__username=username)
    return orders.values_list("user__username", )
