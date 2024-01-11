from django.db import transaction

from db.models import Ticket, Order, MovieSession, User


def create_order(tickets: list[dict],
                 username: str,
                 date: str | None = None
                 ) -> None:
    with transaction.atomic():
        curr_order = Order.objects.create(
            user=User.objects.get(username=username),
        )

        if date:
            curr_order.created_at = date
            curr_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                order=curr_order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str | None = None
               ) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()


def delete_order_by_id(order_id: int) -> None:
    Order.objects.get(id=order_id).delete()
