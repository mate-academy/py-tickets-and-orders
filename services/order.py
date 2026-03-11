from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from datetime import datetime
from db.models import Order, Ticket

@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    User = get_user_model()
    user = User.objects.get(username=username)
    
    if date:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user)
        Order.objects.filter(id=order.id).update(created_at=date)
        order.refresh_from_db()
    else:
        order = Order.objects.create(user=user)
        
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order

def get_orders(
    username: str = None,
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
