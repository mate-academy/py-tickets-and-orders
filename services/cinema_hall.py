from db.models import CinemaHall


def get_cinema_halls() -> list[CinemaHall]:
    return list(CinemaHall.objects.all())
