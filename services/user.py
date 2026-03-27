from datetime import timezone
from django.db import transaction
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, User


def create_order(tickets: list, username: str, date: str = None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"error": f"User with username '{username}' not found."}

    parsed_date = parse_datetime(date) if date else None
    if date and not parsed_date:
        return {"error": "Invalid date format. Expected format: YYYY-MM-DD HH:MM:SS"}

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=parsed_date or timezone.now())
        for ticket_data in tickets:
            Ticket.objects.create(order=order, **ticket_data)

    return {"success": f"Order created successfully for {username}."}


def get_user(user_id):
    return User.objects.filter(id=user_id).first()

def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user