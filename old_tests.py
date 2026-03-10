from django.test import TestCase
from db.models import User, Actor, Genre


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(name="Action")
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.actor = Actor.objects.create(name="John Doe")
        self.actor.genres.add(self.genre)

    def test_user_created(self) -> None:
        self.assertEqual(User.objects.count(), 1)

    def test_genre_created(self) -> None:
        self.assertEqual(Genre.objects.count(), 1)

    def test_actor_genre_relation(self) -> None:
        self.assertIn(self.genre, self.actor.genres.all())
