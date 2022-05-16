from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Genre


class GenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Genre.objects.create(
            name="Comedy",
        )
        Genre.objects.create(
            name="Drama",
        )

    def test_get_genres(self):
        response = self.client.get("/api/cinema/genres/")
        genres = [genre["name"] for genre in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(genres), ["Comedy", "Drama"])

    def test_post_genres(self):
        response = self.client.post(
            "/api/cinema/genres/",
            {
                "name": "Sci-fi",
            },
        )
        db_genres = Genre.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_genres.count(), 3)
        self.assertEqual(db_genres.filter(name="Sci-fi").count(), 1)

    def test_get_invalid_genre(self):
        response = self.client.get("/api/cinema/genres/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_genre(self):
        response = self.client.put(
            "/api/cinema/genres/1/",
            {
                "name": "Sci-fi",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1/",
        )
        db_genres_id_1 = Genre.objects.filter(id=1)
        self.assertEqual(db_genres_id_1.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1000/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
