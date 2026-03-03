from django.db.models import QuerySet
from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order_ticket = Order(user=user)
        order_ticket.save()
        if date:
            created_at_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order_ticket.created_at = created_at_date
            order_ticket.save()

        ticket_list = []
        for ticket in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
                ticket_list.append(Ticket(row=ticket["row"],
                                          seat=ticket["seat"],
                                          movie_session=movie_session,
                                          order=order_ticket))

            except MovieSession.DoesNotExist:
                raise Exception(
                    f"MovieSession with the "
                    f"id {ticket['movie_session']} does not exist")
        try:
            Ticket.objects.bulk_create(ticket_list)
        except Ticket.DoesNotExist as e:
            raise Exception(f"Error creating tickets: {str(e)}")


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
