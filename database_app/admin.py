from django.contrib import admin
from .models import Movie, Actor, Genre, CinemaHall, MovieSession, Order, Ticket, User

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(CinemaHall)
admin.site.register(MovieSession)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(User)
