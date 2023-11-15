from db.models import Ticket
from datetime import datetime


def create_order(tickets: list[dict]) -> None: # username: str, date: datetime = None
    for ticket in tickets:
