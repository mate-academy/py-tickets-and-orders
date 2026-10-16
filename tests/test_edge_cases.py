import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from db.models import CinemaHall, Movie, MovieSession, Order, Ticket
from services.order import create_order
from services.user import create_user, update_user


pytestmark = pytest.mark.django_db


@pytest.fixture
def booking_session():
    return MovieSession.objects.create(
        show_time="2026-10-16 19:00",
        movie=Movie.objects.create(title="Example", description="Example"),
        cinema_hall=CinemaHall.objects.create(
            name="Small", rows=2, seats_in_row=3
        ),
    )


@pytest.mark.parametrize("row,seat", [(0, 1), (-1, 1), (1, 0), (1, -1)])
def test_reject_nonpositive_seats(booking_session, row, seat):
    order = Order.objects.create(user=create_user("customer", "secret"))
    with pytest.raises(ValidationError):
        Ticket.objects.create(
            order=order, movie_session=booking_session, row=row, seat=seat
        )
    assert not Ticket.objects.exists()


def test_last_seat_and_database_uniqueness(booking_session):
    order = Order.objects.create(user=create_user("customer", "secret"))
    ticket = Ticket.objects.create(
        order=order, movie_session=booking_session, row=2, seat=3
    )
    with pytest.raises(IntegrityError), transaction.atomic():
        Ticket.objects.bulk_create([
            Ticket(
                order=order, movie_session=booking_session, row=2, seat=3
            )
        ])
    ticket.save()
    assert Ticket.objects.count() == 1


@pytest.mark.parametrize("last_seat", [1, 4])
def test_later_ticket_failure_rolls_back_whole_order(
    booking_session, last_seat
):
    create_user("customer", "secret")
    with pytest.raises(ValidationError):
        create_order(
            tickets=[
                {"movie_session": booking_session.pk, "row": 1, "seat": 1},
                {
                    "movie_session": booking_session.pk,
                    "row": 1,
                    "seat": last_seat,
                },
            ],
            username="customer",
        )
    assert not Order.objects.exists()
    assert not Ticket.objects.exists()


def test_user_can_clear_optional_fields():
    user = create_user(
        "customer", "secret", email="customer@example.com", first_name="Name"
    )
    update_user(user.pk, email="", first_name="")
    user.refresh_from_db()
    assert user.email == ""
    assert user.first_name == ""
    assert user.check_password("secret")
