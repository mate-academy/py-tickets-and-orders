from django.db.models import QuerySet

from db.models import Ticket, User, Order, MovieSession

from django.db import transaction

from django.core.exceptions import ValidationError

from datetime import datetime


def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:
    try:
        with transaction.atomic():
            user = User.objects.get(username=username)
            created_at = datetime.strptime(date,
                                           "%Y-%m-%d %H:%M") if date else None
            order = Order.objects.create(user=user, created_at=created_at)
            for ticket in tickets:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
                Ticket.objects.create(
                    order=order,
                    movie_session=movie_session,
                    row=ticket["row"],
                    seat=ticket["seat"]
                )
            return order
    except User.DoesNotExist:
        raise ValueError("User not found")
    except MovieSession.DoesNotExist:
        raise ValueError("Movie session not found")
    except ValidationError as e:
        raise ValidationError(e)


def get_orders(username: str = None) -> QuerySet:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            raise ValueError("User not found")
    return Order.objects.all()
