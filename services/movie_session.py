from django.db import transaction
from db.models import Ticket, MovieSession, Movie, CinemaHall
from datetime import datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist

def create_movie_session(movie: Movie, show_time: datetime, cinema_hall: CinemaHall) -> MovieSession:
    movie_session = MovieSession(movie=movie, show_time=show_time, cinema_hall=cinema_hall)
    movie_session.save()
    return movie_session

def update_movie_session(session_id: int, new_movie: Movie = None, new_show_time: datetime = None, new_cinema_hall: CinemaHall = None) -> MovieSession:
    try:
        movie_session = MovieSession.objects.get(id=session_id)
    except ObjectDoesNotExist:
        raise ValidationError(f"Movie session with ID {session_id} does not exist.")

    if new_movie:
        movie_session.movie = new_movie
    if new_show_time:
        movie_session.show_time = new_show_time
    if new_cinema_hall:
        movie_session.cinema_hall = new_cinema_hall

    movie_session.save()
    return movie_session

def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.filter(id=session_id).delete()

def get_taken_seats(movie_session_id: int) -> list[dict]:
    all_taken_tickets = Ticket.objects.filter(movie_session__id=movie_session_id)
    return [{"row": ticket.row, "seat": ticket.seat} for ticket in all_taken_tickets]
