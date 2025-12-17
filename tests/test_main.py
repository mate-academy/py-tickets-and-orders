import sys
import os
import pytest
import datetime

sys.path.append(os.getcwd())

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

from db.models import (
    Actor,
    Genre,
    Movie,
    MovieSession,
    CinemaHall,
    Order,
    Ticket
)
from services.movie import get_movies, create_movie
from services.movie_session import get_taken_seats
from services.user import create_user, get_user, update_user
from services.order import create_order, get_orders

pytestmark = pytest.mark.django_db


@pytest.fixture()
def genres_data():
    Genre.objects.all().delete()
    Genre.objects.create(name="Action")
    Genre.objects.create(name="Drama")
    Genre.objects.create(name="Western")


@pytest.fixture()
def actors_data():
    Actor.objects.all().delete()
    Actor.objects.create(first_name="Keanu", last_name="Reeves")
    Actor.objects.create(first_name="Scarlett", last_name="Johansson")
    Actor.objects.create(first_name="George", last_name="Clooney")


@pytest.fixture()
def movies_data(genres_data, actors_data):
    Movie.objects.all().delete()
    matrix = Movie.objects.create(title="Matrix", description="Matrix movie")
    matrix.actors.add(1, 2)
    matrix.genres.add(1)

    matrix2 = Movie.objects.create(title="Matrix 2", description="Matrix 2 movie")
    matrix2.actors.add(2)
    matrix2.genres.add(1)

    batman = Movie.objects.create(title="Batman", description="Batman movie")
    batman.actors.add(3)
    batman.genres.add(2)

    titanic = Movie.objects.create(title="Titanic", description="Titanic movie")
    titanic.genres.add(1, 2)

    good_bad = Movie.objects.create(title="The Good, the Bad and the Ugly",
                                    description="The Good, the Bad and the Ugly movie")
    good_bad.genres.add(3)

    Movie.objects.create(title="Harry Potter 1")
    Movie.objects.create(title="Harry Potter 2")
    Movie.objects.create(title="Harry Potter 3")
    Movie.objects.create(title="Harry Kasparov: Documentary")


@pytest.fixture()
def cinema_halls_data():
    CinemaHall.objects.all().delete()
    CinemaHall.objects.create(name="Blue", rows=10, seats_in_row=12)
    CinemaHall.objects.create(name="VIP", rows=4, seats_in_row=6)
    CinemaHall.objects.create(name="Cheap", rows=15, seats_in_row=27)


@pytest.fixture()
def movie_sessions_data(movies_data, cinema_halls_data):
    MovieSession.objects.all().delete()
    MovieSession.objects.create(show_time="2019-08-19 20:30", cinema_hall_id=1, movie_id=1)
    MovieSession.objects.create(show_time="2017-08-19 11:10", cinema_hall_id=3, movie_id=4)
    MovieSession.objects.create(show_time="2021-04-03 13:50", cinema_hall_id=2, movie_id=5)
    MovieSession.objects.create(show_time="2021-04-03 16:30", cinema_hall_id=3, movie_id=1)


@pytest.fixture()
def users_data():
    get_user_model().objects.all().delete()
    get_user_model().objects.create_user(username="user1", password="pass1234")
    get_user_model().objects.create_user(username="user2", password="pass1234")


@pytest.fixture()
def orders_data(users_data):
    Order.objects.all().delete()
    for ind, order in enumerate([
        Order.objects.create(id=1, user_id=1),
        Order.objects.create(id=2, user_id=1),
        Order.objects.create(id=3, user_id=2)
    ]):
        order.created_at = datetime.datetime(2020, 11, 1 + ind, 0, 0)
        order.save()


@pytest.fixture()
def tickets_data(movie_sessions_data, orders_data):
    Ticket.objects.all().delete()
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=10)
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=11)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=5)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=6)


@pytest.fixture()
def tickets():
    return [
        {"row": 10, "seat": 8, "movie_session": 1},
        {"row": 10, "seat": 9, "movie_session": 1},
    ]


@pytest.fixture()
def create_order_data():
    Movie.objects.all().delete()
    CinemaHall.objects.all().delete()
    MovieSession.objects.all().delete()
    Order.objects.all().delete()
    Ticket.objects.all().delete()
    get_user_model().objects.all().delete()

    movie = Movie.objects.create(title="Speed", description="Description")
    cinema_hall = CinemaHall.objects.create(name="Blue", rows=14, seats_in_row=12)
    MovieSession.objects.create(show_time=datetime.datetime.now(), movie=movie, cinema_hall=cinema_hall)
    get_user_model().objects.create_user(username="user_1")


@pytest.mark.django_db(transaction=True)
def test_order_service_create_order_without_date(create_order_data, tickets):
    create_order(tickets=tickets, username="user_1")
    usernames = list(Order.objects.all().values_list("user__username", flat=True))
    assert usernames == ["user_1"]
