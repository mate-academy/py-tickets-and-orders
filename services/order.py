from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.utils.timezone import make_aware

from db.models import User
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    try:
        with transaction.atomic():
            user = User.objects.get(username=username)

            if date:
                created_at = make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))
                order = Order.objects.create(user=user, created_at=created_at)
            else:
                order = Order.objects.create(user=user)

            ticket_objects = []
            for ticket in tickets:
                movie_session = MovieSession.objects.get(id=ticket["movie_session"])
                # Check if the seat is already taken
                if Ticket.objects.filter(
                        movie_session=movie_session, row=ticket["row"], seat=ticket["seat"]
                ).exists():
                    raise ValueError(f"Seat ({ticket['row']}, {ticket['seat']}) is already taken.")

                ticket_objects.append(
                    Ticket(
                        row=ticket["row"],
                        seat=ticket["seat"],
                        movie_session=movie_session,
                        order=order,
                    )
                )

            Ticket.objects.bulk_create(ticket_objects)
            return order
    except ObjectDoesNotExist as e:
        raise Http404(f"Specified object does not exist: {e}")
    except ValueError as e:
        raise ValueError(f"Validation error: {e}")


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
