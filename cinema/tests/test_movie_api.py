from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import Movie, Genre, Actor


class MovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drama = Genre.objects.create(
            name="Drama",
        )
        self.comedy = Genre.objects.create(
            name="Comedy",
        )
        self.actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(self.drama)
        self.movie.genres.add(self.comedy)
        self.movie.actors.add(self.actress)

    def test_get_movies(self):
        movies = self.client.get("/api/cinema/movies/")
        titanic = {
            "title": "Titanic",
            "description": "Titanic description",
            "duration": 123,
            "genres": ["Drama", "Comedy"],
            "actors": ["Kate Winslet"],
        }
        print(movies.data)
        self.assertEqual(movies.status_code, status.HTTP_200_OK)
        for field in titanic:
            self.assertEqual(movies.data[0][field], titanic[field])

    def test_get_movies_with_genre_filtering(self):
        movies = self.client.get(f"/api/cinema/movies/?genres={self.comedy.id}")
        self.assertEqual(len(movies.data), 1)
        movies = self.client.get(f"/api/cinema/movies/?genres={123213}")
        self.assertEqual(len(movies.data), 0)

    def test_get_movies_with_actors_filtering(self):
        movies = self.client.get(f"/api/cinema/movies/?actors={self.actress.id}")
        self.assertEqual(len(movies.data), 1)
        movies = self.client.get(f"/api/cinema/movies/?actors={123}")
        self.assertEqual(len(movies.data), 0)

    def test_get_movies_with_title_filtering(self):
        movies = self.client.get(f"/api/cinema/movies/?title=ita")
        self.assertEqual(len(movies.data), 1)
        movies = self.client.get(f"/api/cinema/movies/?title=ati")
        self.assertEqual(len(movies.data), 0)

    def test_post_movies(self):
        movies = self.client.post(
            "/api/cinema/movies/",
            {
                "title": "Superman",
                "description": "Superman description",
                "duration": 123,
                "actors": [1],
                "genres": [1, 2],
            },
        )
        db_movies = Movie.objects.all()
        self.assertEqual(movies.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_movies.count(), 2)
        self.assertEqual(db_movies.filter(title="Superman").count(), 1)

    def test_post_invalid_movies(self):
        movies = self.client.post(
            "/api/cinema/movies/",
            {
                "title": "Superman",
                "description": "Superman description",
                "duration": 123,
                "actors": [
                    {
                        "id": 3,
                    }
                ],
            },
        )
        superman_movies = Movie.objects.filter(title="Superman")
        self.assertEqual(movies.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(superman_movies.count(), 0)

    def test_get_movie(self):
        response = self.client.get("/api/cinema/movies/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Titanic")
        self.assertEqual(response.data["description"], "Titanic description")
        self.assertEqual(response.data["duration"], 123)
        self.assertEqual(response.data["genres"][0]["name"], "Drama")
        self.assertEqual(response.data["genres"][1]["name"], "Comedy")
        self.assertEqual(response.data["actors"][0]["first_name"], "Kate")
        self.assertEqual(response.data["actors"][0]["last_name"], "Winslet")
        self.assertEqual(response.data["actors"][0]["full_name"], "Kate Winslet")

    def test_get_invalid_movie(self):
        response = self.client.get("/api/cinema/movies/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_movie(self):
        self.client.put(
            "/api/cinema/movies/1/",
            {
                "title": "Watchman",
                "description": "Watchman description",
                "duration": 321,
                "genres": [1, 2],
                "actors": [1],
            },
        )
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(
            [db_movie.title, db_movie.description],
            [
                "Watchman",
                "Watchman description",
            ],
        )
        self.assertEqual(db_movie.title, "Watchman")

    def test_delete_movie(self):
        response = self.client.delete(
            "/api/cinema/movies/1/",
        )
        db_movies_id_1 = Movie.objects.filter(id=1)
        self.assertEqual(db_movies_id_1.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_movie(self):
        response = self.client.delete(
            "/api/cinema/movies/1000/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
