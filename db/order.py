from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from typing import List, Optional, Dict, Any
import datetime

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: List[Dict[str, Any]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError("User with provided username does not exist")

    try:
        created_at = (
            datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            if date
            else datetime.datetime.now()
        )
    except ValueError:
        raise ValueError("Invalid date format. Expected: YYYY-MM-DD HH:MM")

    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )
    for ticket_data in tickets:
        try:
            session = MovieSession.objects.get(id=ticket_data["movie_session"])
            Ticket.objects.create(
                movie_session=session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
        except ObjectDoesNotExist:
            raise ValueError(
                f"Movie session with ID "
                f"{ticket_data["movie_session"]} does not exist"
            )
        except ValidationError as e:
            raise ValueError(f"Invalid ticket data: {str(e)}")
    return order


def get_orders(
    username: Optional[str] = None,
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
