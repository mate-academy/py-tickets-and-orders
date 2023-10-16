from datetime import datetime
from typing import List, Union
from django.db import transaction
from typing import Optional

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: Optional[str] = None
) -> Union[Order, None]:
    work_user = User.objects.filter(username=username).first()
    if work_user:
        new_order = Order.objects.create(
            user=work_user
        )
        if date:
            date_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
            new_order.created_at = date_time
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session_id=ticket["movie_session"]
            )

        return new_order


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
