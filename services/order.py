from django.db import transaction

from db.models import Order, User, Ticket


@transaction.atomic()
def create_order(tickets: list,
                 username: str,
                 date: str = None
                 ) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order_id=order.id,
            seat=ticket["seat"],
            row=ticket["row"],
        )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
