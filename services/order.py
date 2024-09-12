from django.db import transaction
from datetime import datetime

from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = datetime.now().strftime("%Y-%m-%d %H:%M"),
) -> None:
    new_order = Order(
        user=User.objects.get(username=username),
        created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")
    )
    print(new_order.created_at)
    new_order.save()
    print(new_order.created_at)
    Ticket.objects.bulk_create(
        [
            Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets
        ]
    )


def get_orders(username: str = None) -> list[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
