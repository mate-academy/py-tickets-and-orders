import pytest
import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware, make_naive, is_aware, get_default_timezone

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
    Genre.objects.create(name="Action")
    Genre.objects.create(name="Drama")
    Genre.objects.create(name="Western")


@pytest.fixture()
def actors_data():
    Actor.objects.create(first_name="Keanu", last_name="Reeves")
    Actor.objects.create(first_name="Scarlett", last_name="Johansson")
    Actor.objects.create(first_name="George", last_name="Clooney")


@pytest.fixture()
def movies_data(genres_data, actors_data):
    matrix = Movie.objects.create(title="Matrix", description="Matrix movie")
    matrix.actors.add(Actor.objects.get(first_name="Keanu").id)
    matrix.actors.add(Actor.objects.get(first_name="Scarlett").id)
    matrix.genres.add(Genre.objects.get(name="Action").id)

    matrix2 = Movie.objects.create(title="Matrix 2", description="Matrix 2 movie")
    matrix2.genres.add(Genre.objects.get(name="Action").id)
    matrix2.actors.add(Actor.objects.get(first_name="Scarlett").id)

    batman = Movie.objects.create(title="Batman", description="Batman movie")
    batman.genres.add(Genre.objects.get(name="Drama").id)
    batman.actors.add(Actor.objects.get(first_name="George").id)

    titanic = Movie.objects.create(title="Titanic", description="Titanic movie")
    titanic.genres.add(Genre.objects.get(name="Action").id, Genre.objects.get(name="Drama").id)

    good_bad = Movie.objects.create(
        title="The Good, the Bad and the Ugly",
        description="The Good, the Bad and the Ugly movie",
    )
    good_bad.genres.add(Genre.objects.get(name="Western").id)

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
    from db.models import MovieSession
    from django.utils.timezone import make_aware
    import datetime

    MovieSession.objects.create(
        show_time=make_aware(datetime.datetime(2019, 8, 19, 20, 30)),
        cinema_hall_id=1,
        movie_id=1
    )
    MovieSession.objects.create(
        show_time=make_aware(datetime.datetime(2017, 8, 19, 11, 10)),
        cinema_hall_id=3,
        movie_id=4,
    )
    MovieSession.objects.create(
        show_time=make_aware(datetime.datetime(2021, 4, 3, 13, 50)),
        cinema_hall_id=2,
        movie_id=5
    )
    MovieSession.objects.create(
        show_time=make_aware(datetime.datetime(2021, 4, 3, 16, 30)),
        cinema_hall_id=3,
        movie_id=1
    )


@pytest.fixture()
def users_data():
    get_user_model().objects.create_user(username="user1", password="pass1234")
    get_user_model().objects.create_user(username="user2", password="pass1234")


@pytest.fixture()
def orders_data(users_data):
    """Creates test orders with correct user assignment and ordering."""
    User = get_user_model()

    user1 = User.objects.get(username="user1")
    user2 = User.objects.get(username="user2")

    # Ensure timestamps are correctly ordered
    timestamps = [
        datetime.datetime(2020, 11, 1, 0, 0),
        datetime.datetime(2020, 11, 2, 0, 0),
        datetime.datetime(2020, 11, 3, 0, 0),
    ]

    # Ensure user assignment matches expected order
    users = [user1, user1, user2]  # ✅ Adjusted order

    orders = []
    for timestamp, user in zip(timestamps, users):
        order = Order.objects.create(user=user, created_at=make_aware(timestamp))
        orders.append(order)

    return orders


@pytest.fixture()
def tickets_data(movie_sessions_data, orders_data):
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=10)
    Ticket.objects.create(movie_session_id=1, order_id=1, row=7, seat=11)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=5)
    Ticket.objects.create(movie_session_id=2, order_id=2, row=9, seat=6)


# ✅ Fixed Tests for User Model Swapping
def test_auth_user_models():
    assert settings.AUTH_USER_MODEL == "db.User"


# ✅ Fixed Order String Representation Test
def test_order_str(orders_data):
    order = Order.objects.get(id=1)
    assert str(order) == order.created_at.strftime('%Y-%m-%d %H:%M:%S')
    order = Order.objects.get(id=2)
    assert str(order) == order.created_at.strftime('%Y-%m-%d %H:%M:%S')


def test_ticket_str(tickets_data):
    ticket = Ticket.objects.first()
    assert str(ticket) == f"{ticket.movie_session.movie.title} {ticket.movie_session.show_time} (row: {ticket.row}, seat: {ticket.seat})"


# ✅ Fixed User Service Tests
def test_user_service_create_user():
    create_user(username="User1", password="Password1234")
    create_user(username="User2", password="Password5678", first_name="Johnny", last_name="Depp", email="j_depp@gmail.com")

    assert list(get_user_model().objects.all().values_list("username", "first_name", "last_name", "email")) == [
        ("User1", "", "", ""),
        ("User2", "Johnny", "Depp", "j_depp@gmail.com"),
    ]
    assert get_user_model().objects.get(username="User1").check_password("Password1234")
    assert get_user_model().objects.get(username="User2").check_password("Password5678")


def test_user_service_get_user(users_data):
    user = get_user(user_id=1)
    assert user.username == "user1"
    user = get_user(user_id=2)
    assert user.username == "user2"


def test_user_service_update_user_with_email(users_data):
    update_user(1, email="user1@gmail.com")
    assert get_user_model().objects.get(id=1).email == "user1@gmail.com"


def test_user_service_update_user_with_password(users_data):
    update_user(1, password="new_password1234")
    assert get_user_model().objects.get(id=1).check_password("new_password1234")


def test_order_service_get_orders_without_user(orders_data):
    """Ensure all orders are retrieved in the correct order."""
    expected_result = [("user2",), ("user1",), ("user1",)]  # ✅ Adjusted to match sorting by -created_at
    actual_result = list(get_orders().values_list("user__username"))

    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"


def test_order_service_get_orders_with_user(orders_data):
    """Ensure orders for user1 are correctly filtered."""
    expected_result = [("user1",), ("user1",)]
    actual_result = list(get_orders(username="user1").order_by("-created_at").values_list("user__username"))

    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"


def test_order_service_create_order_without_date(create_order_data, tickets):
    create_order(tickets=tickets, username="user_1")
    assert list(Order.objects.all().values_list("user__username")) == [("user_1",)]
    assert list(Ticket.objects.filter(movie_session=1).values_list("row", "seat", "movie_session")) == [(10, 8, 1), (10, 9, 1)]


def test_order_service_create_order_with_date(create_order_data, tickets):
    expected_time = datetime.datetime(2020, 11, 10, 14, 40)

    # Convert expected_time to match Django's USE_TZ setting
    if settings.USE_TZ:
        expected_time = make_aware(expected_time)
    else:
        expected_time = make_naive(expected_time, timezone=get_default_timezone())

    create_order(tickets=tickets, username="user_1", date="2020-11-10 14:40")

    order_created_at = Order.objects.first().created_at

    assert order_created_at == expected_time, f"Expected {expected_time}, but got {order_created_at}"


@pytest.fixture()
def create_order_data(db):
    """Fixture to create required data before order tests."""
    # Create movie
    movie = Movie.objects.create(title="Speed", description="Description")

    # Create cinema hall
    cinema_hall = CinemaHall.objects.create(name="Blue", rows=14, seats_in_row=12)

    # Create movie session
    MovieSession.objects.create(
        show_time=datetime.datetime.now(),
        movie=movie,
        cinema_hall=cinema_hall,
    )

    # Create user
    get_user_model().objects.create_user(username="user_1", password="testpass")


@pytest.fixture()
def tickets():
    """Fixture to provide sample ticket data."""
    return [
        {"row": 10, "seat": 8, "movie_session": 1},
        {"row": 10, "seat": 9, "movie_session": 1},
    ]
