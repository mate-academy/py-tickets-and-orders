import pytest
import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

from db.models import (
    Movie,
    MovieSession,
    CinemaHall,
    Order,
    Ticket,
)
from services.movie import get_movies, create_movie
from services.movie_session import get_taken_seats
from services.user import create_user, get_user, update_user
from services.order import create_order, get_orders


pytestmark = pytest.mark.django_db


@pytest.fixture()
def movies_data():
    Movie.objects.create(title="Matrix", description="Matrix movie")
    Movie.objects.create(title="Matrix 2", description="Matrix 2 movie")
    Movie.objects.create(title="Batman", description="Batman movie")
    Movie.objects.create(title="Titanic", description="Titanic movie")
    Movie.objects.create(title="The Good, the Bad and the Ugly",
                         description="Western classic")
    Movie.objects.create(title="Harry Potter 1")
    Movie.objects.create(title="Harry Potter 2")
    Movie.objects.create(title="Harry Potter 3")
    Movie.objects.create(title="Harry Kasparov: Documentary")


@pytest.fixture()
def cinema_halls_data():
    CinemaHall.objects.create(name="Blue", rows=10, seats_in_row=12)
    CinemaHall.objects.create(name="VIP", rows=4, seats_in_row=6)
    CinemaHall.objects.create(name="Cheap", rows=15, seats_in_row=27)


@pytest.fixture()
def movie_sessions_data(movies_data, cinema_halls_data):
    MovieSession.objects.create(
        show_time="2019-08-19 20:30",
        cinema_hall_id=1,
        movie_id=1
    )
    MovieSession.objects.create(
        show_time="2017-08-19 11:10",
        cinema_hall_id=3,
        movie_id=4
    )
    MovieSession.objects.create(
        show_time="2021-04-03 13:50",
        cinema_hall_id=2,
        movie_id=5
    )
    MovieSession.objects.create(
        show_time="2021-04-03 16:30",
        cinema_hall_id=3,
        movie_id=1
    )


@pytest.fixture()
def users_data():
    get_user_model().objects.create_user(username="user1", password="pass1234")
    get_user_model().objects.create_user(username="user2", password="pass1234")


@pytest.fixture()
def orders_data(users_data):
    for ind, order in enumerate([
        Order.objects.create(id=1, user_id=1),
        Order.objects.create(id=2, user_id=1),
        Order.objects.create(id=3, user_id=2)
    ]):
        order.created_at = datetime.datetime(2020, 11, 1 + ind, 0, 0)
        order.save()


@pytest.fixture()
def tickets_data(movie_sessions_data, orders_data):
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=10)
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=11)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=5)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=6)


def test_auth_user_models():
    assert settings.AUTH_USER_MODEL == "db.User"


def test_order_str(orders_data):
    order = Order.objects.get(id=1)
    assert str(order) == f"<Order: {order.created_at}>"


def test_ticket_clean_row_out_of_range(movie_sessions_data, orders_data):
    with pytest.raises(ValidationError) as e_info:
        Ticket.objects.create(movie_session_id=1, order_id=1, row=11, seat=5)
    assert "row number must be in available range" in str(e_info.value)


def test_ticket_clean_seat_out_of_range(movie_sessions_data, orders_data):
    with pytest.raises(ValidationError) as e_info:
        Ticket.objects.create(movie_session_id=1, order_id=1, row=10, seat=13)
    assert "seat number must be in available range" in str(e_info.value)
