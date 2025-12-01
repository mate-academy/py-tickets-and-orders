import pytest
import datetime

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
from services.movie_session import (
    get_taken_seats,
)
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
    matrix.actors.add(1)
    matrix.actors.add(2)
    matrix.genres.add(1)

    matrix2 = Movie.objects.create(title="Matrix 2",
                                   description="Matrix 2 movie")
    matrix2.genres.add(1)
    matrix2.actors.add(2)

    batman = Movie.objects.create(title="Batman",
                                  description="Batman movie")
    batman.genres.add(2)
    batman.actors.add(3)

    titanic = Movie.objects.create(title="Titanic",
                                   description="Titanic movie")
    titanic.genres.add(1, 2)

    good_bad = Movie.objects.create(
        title="The Good, the Bad and the Ugly",
        description="The Good, the Bad and the Ugly movie",
    )
    good_bad.genres.add(3)

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
        show_time="2019-8-19 20:30",
        cinema_hall_id=1,
        movie_id=1
    )
    MovieSession.objects.create(
        show_time="2017-8-19 11:10",
        cinema_hall_id=3,
        movie_id=4,
    )
    MovieSession.objects.create(
        show_time="2021-4-3 13:50", cinema_hall_id=2, movie_id=5
    )

    MovieSession.objects.create(
        show_time="2021-4-3 16:30", cinema_hall_id=3, movie_id=1
    )


@pytest.fixture()
def users_data():
    get_user_model().objects.create_user(username="user1",
                                         password="pass1234")
    get_user_model().objects.create_user(username="user2",
                                         password="pass1234")


@pytest.fixture()
def orders_data(users_data):
    for ind, order in enumerate([
        Order.objects.create(id=1, user_id=1),
        Order.objects.create(id=2, user_id=1),
        Order.objects.create(id=3, user_id=2)
    ]):
        order.created_at = datetime.datetime(
            2020, 11, 1 + ind, 0, 0
        )
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
    assert str(order) == str(order.created_at)
    order = Order.objects.get(id=2)
    assert str(order) == str(order.created_at)


def test_order_ordering(orders_data):
    assert list(
        Order.objects.all().values_list("id")
    ) == list(
        Order.objects.all().order_by("-created_at").values_list("id")
    )


def test_ticket_str(tickets_data):
    assert str(
        Ticket.objects.first()
    ) == "Matrix 2019-08-19 20:30:00 (row: 7, seat: 10)"


def test_ticket_unique_constraint(tickets_data):
    Ticket.objects.create(order_id=1, movie_session_id=1, row=9, seat=9)
    with pytest.raises(ValidationError):
        Ticket.objects.create(order_id=1, movie_session_id=1, row=9, seat=9)


def test_movie_service_get_movies_with_title(movies_data):
    assert list(get_movies(title="harry").values_list("title")) == [
        ("Harry Potter 1",),
        ("Harry Potter 2",),
        ("Harry Potter 3",),
        ("Harry Kasparov: Documentary",),
    ]

    assert list(get_movies(title="harry potter").values_list("title")) == [
        ("Harry Potter 1",),
        ("Harry Potter 2",),
        ("Harry Potter 3",),
    ]


def test_movie_service_get_movies_with_full_data(movies_data):
    assert list(get_movies(
        genres_ids=[1, 2], actors_ids=[2, 3], title="matrix"
    ).values_list("title")) == [("Matrix",), ("Matrix 2",)]
    assert list(get_movies(
        genres_ids=[1, 2], actors_ids=[2, 3], title="batman"
    ).values_list("title")) == [("Batman",)]


def test_movie_session_service_get_taken_seats(tickets_data):
    assert get_taken_seats(movie_session_id=1) == [
        {"row": 7, "seat": 10},
        {"row": 7, "seat": 11},
    ]
    assert get_taken_seats(movie_session_id=2) == [
        {"row": 9, "seat": 5},
        {"row": 9, "seat": 6},
    ]


def test_user_service_create_user():
    create_user(username="User1", password="Password1234")
    create_user(
        username="User2",
        password="Password5678",
        first_name="Johnny",
        last_name="Depp",
        email="j_depp@gmail.com",
    )
    assert list(
        get_user_model()
        .objects.all()
        .values_list("username", "first_name", "last_name", "email")
    ) == [("User1", "", "", ""),
          ("User2", "Johnny", "Depp", "j_depp@gmail.com")]
    assert (get_user_model().objects.get(
        username="User1"
    ).password != "Password1234"), "Password should be encrypted"
    assert (get_user_model().objects.get(
        username="User2"
    ).password != "Password5678"), "Password should be encrypted"


def test_user_service_get_user(users_data):
    user = get_user(user_id=1)
    assert user.username == "user1"
    user = get_user(user_id=2)
    assert user.username == "user2"


def test_user_service_update_user_with_no_data(users_data):
    user1_password = get_user_model().objects.get(id=1).password
    update_user(user_id=1)
    assert list(
        get_user_model()
        .objects.filter(id=1)
        .values_list("username", "first_name", "last_name", "email")
    ) == [
        ("user1", "", "", ""),
    ]
    assert get_user_model().objects.get(id=1).password == user1_password


def test_user_service_update_user_with_email(users_data):
    user1_password = get_user_model().objects.get(id=1).password
    update_user(1, email="user1@gmail.com")
    assert list(
        get_user_model()
        .objects.filter(id=1)
        .values_list("username", "first_name", "last_name", "email")
    ) == [
        ("user1", "", "", "user1@gmail.com"),
    ]
    assert get_user_model().objects.get(id=1).password == user1_password


def test_user_service_update_user_with_password(users_data):
    update_user(1, password="new_password1234")
    assert list(
        get_user_model()
        .objects.filter(id=1)
        .values_list("username", "first_name", "last_name", "email")
    ) == [
        ("user1", "", "", ""),
    ]
    assert get_user_model().objects.get(id=1).check_password(
        "new_password1234"
    )


def test_user_service_update_user_with_whole_data(users_data):
    update_user(
        1,
        username="New_user1",
        password="new_password1234",
        email="user1_@gmail.com",
        first_name="Johnny",
        last_name="Depp",
    )
    assert list(
        get_user_model()
        .objects.filter(id=1)
        .values_list("username", "first_name", "last_name", "email")
    ) == [
        ("New_user1", "Johnny", "Depp", "user1_@gmail.com"),
    ]
    assert get_user_model().objects.get(id=1).check_password(
        "new_password1234"
    )


def test_order_service_get_orders_without_user(orders_data):
    assert list(get_orders().values_list("user__username")) == [
        ("user2",),
        ("user1",),
        ("user1",),
    ]


def test_order_service_get_orders_with_user(orders_data):
    assert list(get_orders(username="user1").values_list(
        "user__username"
    )) == [
        ("user1",),
        ("user1",),
    ]


@pytest.fixture()
def tickets():
    return [
        {"row": 10, "seat": 8, "movie_session": 1},
        {"row": 10, "seat": 9, "movie_session": 1},
    ]


@pytest.fixture()
def incorrect_tickets():
    return [
        {"row": 10, "seat": 8, "movie_session": 1},
        {"row": 10, "seat": 9, "movie_session": 1},
    ]


@pytest.fixture()
def create_order_data():
    movie = Movie.objects.create(title="Speed", description="Description")
    cinema_hall = CinemaHall.objects.create(name="Blue",
                                            rows=14,
                                            seats_in_row=12)
    MovieSession.objects.create(
        show_time=datetime.datetime.now(),
        movie=movie,
        cinema_hall=cinema_hall,
    )
    get_user_model().objects.create_user(username="user_1")


def test_order_service_create_order_without_date(create_order_data, tickets):
    create_order(tickets=tickets, username="user_1")
    assert list(Order.objects.all().values_list(
        "user__username"
    )) == [("user_1",)]
    assert list(
        Ticket.objects.filter(movie_session=1).values_list(
            "row", "seat", "movie_session"
        )
    ) == [(10, 8, 1), (10, 9, 1)]


def test_order_service_create_order_with_date(create_order_data, tickets):
    create_order(tickets=tickets, username="user_1", date="2020-11-10 14:40")
    assert list(Order.objects.all().values_list(
        "user__username"
    )) == [("user_1",)]
    assert list(
        Ticket.objects.filter(movie_session=1).values_list(
            "row", "seat", "movie_session"
        )
    ) == [(10, 8, 1), (10, 9, 1)]
    assert Order.objects.first().created_at == datetime.datetime(
        2020, 11, 10, 14, 40
    )


def test_create_order_transaction_atomic(tickets):
    get_user_model().objects.create_user(username="user_1")
    with pytest.raises(Exception):
        create_order(tickets=tickets, username="user_1")

    assert Order.objects.all().count() == 0


def test_ticket_clean_row_out_of_range(movie_sessions_data, orders_data):
    with pytest.raises(ValidationError) as e_info:
        Ticket.objects.create(movie_session_id=1, order_id=1, row=11, seat=5)
    assert (
        str(e_info.value) == "{'row': ['row number must be in available "
        "range: (1, rows): (1, 10)']}"
    )


def test_ticket_clean_seat_out_of_range(movie_sessions_data, orders_data):
    with pytest.raises(ValidationError) as e_info:
        Ticket.objects.create(movie_session_id=1, order_id=1, row=10, seat=13)

    assert str(e_info.value) == (
        "{'seat': ['seat number must be in "
        "available range: (1, seats_in_row): "
        "(1, 12)']}"
    )


from django.db import transaction


def test_create_movie_transaction_atomic(genres_data, actors_data):
    with pytest.raises(ValueError):
        with transaction.atomic():
            create_movie(
                movie_title="New movie",
                movie_description="Movie description",
                genres_ids=["zero", 1, 2],
                actors_ids=[1, 2, 3]
            )

    assert Movie.objects.count() == 0
