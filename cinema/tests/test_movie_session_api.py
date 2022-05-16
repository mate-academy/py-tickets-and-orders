import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import Movie, Genre, Actor, MovieSession, CinemaHall, Ticket


class MovieSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        drama = Genre.objects.create(
            name="Drama",
        )
        comedy = Genre.objects.create(
            name="Comedy",
        )
        actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(drama)
        self.movie.genres.add(comedy)
        self.movie.actors.add(actress)
        self.cinema_hall = CinemaHall.objects.create(
            name="White",
            rows=10,
            seats_in_row=14,
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie, cinema_hall=self.cinema_hall, show_time=datetime.datetime.now()
        )

    def test_get_movie_sessions(self):
        movie_sessions = self.client.get("/api/cinema/movie_sessions/")
        movie_session = {
            "movie_title": "Titanic",
            "cinema_hall_name": "White",
            "cinema_hall_capacity": 140,
        }
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        for field in movie_session:
            self.assertEqual(movie_sessions.data[0][field], movie_session[field])

    def test_post_movie_session(self):
        movies = self.client.post(
            "/api/cinema/movie_sessions/",
            {"movie": 1, "cinema_hall": 1, "show_time": datetime.datetime.now()},
        )
        movie_sessions = MovieSession.objects.all()
        self.assertEqual(movies.status_code, status.HTTP_201_CREATED)
        self.assertEqual(movie_sessions.count(), 2)

    def test_get_movie_session(self):
        response = self.client.get("/api/cinema/movie_sessions/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["movie"]["title"], "Titanic")
        self.assertEqual(response.data["movie"]["description"], "Titanic description")
        self.assertEqual(response.data["movie"]["duration"], 123)
        self.assertEqual(response.data["movie"]["genres"], ["Drama", "Comedy"])
        self.assertEqual(response.data["movie"]["actors"], ["Kate Winslet"])
        self.assertEqual(response.data["cinema_hall"]["capacity"], 140)
        self.assertEqual(response.data["cinema_hall"]["rows"], 10)
        self.assertEqual(response.data["cinema_hall"]["seats_in_row"], 14)
        self.assertEqual(response.data["cinema_hall"]["name"], "White")
        self.assertEqual(response.data["tickets"], [])
