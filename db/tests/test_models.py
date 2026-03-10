import pytest
from db.models import User, Genre, Actor


@pytest.mark.django_db
def test_create_user() -> None:
    user = User.objects.create_user(username="test", password="12345")
    assert user.username == "test"


@pytest.mark.django_db
def test_create_genre() -> None:
    genre = Genre.objects.create(name="Action")
    assert genre.name == "Action"


@pytest.mark.django_db
def test_create_actor() -> None:
    actor = Actor.objects.create(name="Tom Hanks", age=65)
    assert actor.age == 65
    assert actor.name == "Tom Hanks"
