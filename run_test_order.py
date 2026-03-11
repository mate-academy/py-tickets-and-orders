import os
import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from services.order import create_order
from db.models import Order
from django.contrib.auth import get_user_model
from db.models import MovieSession, CinemaHall, Movie

User = get_user_model()
try:
    user = User.objects.get(username="user_1")
except:
    user = User.objects.create_user(username="user_1")

movie = Movie.objects.create(title="Speed", description="Description")
cinema_hall = CinemaHall.objects.create(name="Blue", rows=14, seats_in_row=12)
movie_s = MovieSession.objects.create(show_time=datetime.datetime.now(), movie=movie, cinema_hall=cinema_hall)

tickets = [
    {"row": 10, "seat": 8, "movie_session": movie_s.id},
    {"row": 10, "seat": 9, "movie_session": movie_s.id},
]

order = create_order(tickets=tickets, username="user_1", date="2020-11-10 14:40")
print(f"Created at: {repr(order.created_at)}")

