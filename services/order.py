from django.db import transaction
from db.models import Order, Ticket
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

def create_order(tickets: list, username: str, date: str = None):
    try:
        user = User.objects.get(username=username)

        order_date = datetime.strptime(date, "%Y-%m-%d %H:%M") if date else None

        with transaction.atomic():
            order = Order.objects.create(user=user, created_at=order_date)

            ticket_objs = []
            for ticket_data in tickets:
                ticket_objs.append(
                    Ticket(
                        row=ticket_data['row'],
                        seat=ticket_data['seat'],
                        movie_session_id=ticket_data['movie_session'],
                        order=order
                    )
                )
            Ticket.objects.bulk_create(ticket_objs)

            return order
    except Exception as e:
        print(f"Error creating order: {e}")
        return None


def get_orders(username: str = None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()