from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from db.models import Order, Ticket
from db.models import User as UserTyping

UserModel: UserTyping = get_user_model()


@atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    user = UserModel.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    order.save()
    for ticket in tickets:
        movie_session_id = ticket.pop("movie_session")
        ticket_obj = Ticket(
            order=order,
            movie_session_id=movie_session_id,
            **ticket)
        ticket_obj.save()
    return order


def get_orders(username: str = None) -> List[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
