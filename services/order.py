from db.models import Order, User, Ticket
from django.db import transaction
from django.db.models import QuerySet


def create_order(
  tickets: list[dict],
  username: str,
  date: str = None
) -> None:
  with transaction.atomic():
    user = User.objects.get(username=username)
    add_fields = {"user": user}
    if date:
      add_fields["created_at"] = date
    order = Order.objects.create(**add_fields)
  
    for ticket in tickets:
      Ticket.objects.create(order=order, **ticket)

    return order
    
