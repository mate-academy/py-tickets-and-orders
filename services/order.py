from django.contrib.auth.models import User
from django.db import transaction

from db.models import Order


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order
