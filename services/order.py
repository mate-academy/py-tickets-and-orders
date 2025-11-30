from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
import datetime



def create_order(tickets: list[dict],
                 username: str,
                 date: datetime.datetime = None) -> Order:
    try:
        with transaction.atomic():
            user = get_user_model().objects.get(username=username)
            order = Order.objects.create(user=user)
            if date:
                order.created_at = date
                order.save()

            list_of_tickets = []
            for ticket in tickets:
                ticket_obj = Ticket(movie_session_id=ticket["movie_session"],
                                    order=order,
                                    seat=ticket["seat"],
                                    row=ticket["row"])
                ticket_obj.clean()
                list_of_tickets.append(ticket_obj)

            Ticket.objects.bulk_create(list_of_tickets)
            return order
    except IntegrityError:
        raise ValidationError("You can't create the order "
                              "with this/those ticket/tickets")


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return (Order.objects.prefetch_related("user")
                .filter(user__username=username))
    return Order.objects.all()
