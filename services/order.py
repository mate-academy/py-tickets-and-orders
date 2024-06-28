from django.db import transaction
from services.movie_session import get_movie_session_by_id
from db.models import Order, Ticket, User, MovieSession
@transaction.atomic
def create_order(tickets: list, username: str, date: str=None) -> None:
    try:
        user = User.objects.get(username=username)
        if date:
            order = Order.objects.create(
                created_at=date,
                user=user
            )
        else:
            order = Order.objects.create(
                user=user
            )

        order.save()

        for ticket_data in tickets:
            movie_session = get_movie_session_by_id(ticket_data["movie_session"])
            ticket_create = Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
            ticket_create.save()
    except Exception as e:
        print(f"Failed to create order: {e}")

def get_orders(username: str=None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()