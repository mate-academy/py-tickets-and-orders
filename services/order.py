from django.db import transaction

from db.models import User, Ticket, Order, MovieSession


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> Order:

    with transaction.atomic():

        user = User.objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)
        if date:
            order.created_at = date

        order.save()

        for tickets_data in tickets:
            movie_session = MovieSession.objects.get(
                id=tickets_data["movie_session"]
            )

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=tickets_data["row"],
                seat=tickets_data["seat"]
            )
        return order


def get_orders(username: str = None) -> Order:

    if username:
        get_user = User.objects.get(username=username).id
        return Order.objects.filter(user=get_user)

    return Order.objects.all()
