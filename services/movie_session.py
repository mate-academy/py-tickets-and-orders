from db.models import MovieSession, Ticket


def create_movie_session(
    movie_session: dict,
) -> MovieSession:
    return MovieSession.objects.create(
        movie=movie_session.get("movie"),
        show_time=movie_session.get("show_time"),
        cinema_hall=movie_session.get("cinema_hall"),
    )


def update_movie_session(
    session_id: int, movie_session: dict
) -> MovieSession:
    session = MovieSession.objects.get(id=session_id)
    session.movie = movie_session.get("movie", session.movie)
    session.show_time = movie_session.get("show_time", session.show_time)
    session.cinema_hall = movie_session.get("cinema_hall", session.cinema_hall)
    session.save()
    return session


def delete_movie_session_by_id(session_id: int) -> None:
    MovieSession.objects.get(id=session_id).delete()


def get_taken_seats(movie_session_id: int) -> list:
    seats = Ticket.objects.filter(
        movie_session_id=movie_session_id
    ).values("row", "seat")

    return list(seats)
