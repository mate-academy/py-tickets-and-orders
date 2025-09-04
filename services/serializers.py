from rest_framework import serializers
from db.models import Order, MovieSession, Movie, CinemaHall, Ticket


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ["id", "name", "capacity"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "duration"]


class MovieSessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    cinema_hall = CinemaHallSerializer()
    taken_places = serializers.SerializerMethodField()
    tickets_available = serializers.SerializerMethodField()

    class Meta:
        model = MovieSession
        fields = [
            "id",
            "movie",
            "cinema_hall",
            "show_time",
            "taken_places",
            "tickets_available"
        ]

    def get_taken_places(self, obj: MovieSession) -> list[dict]:
        return list(Ticket.objects.filter(movie_session=obj).values(
            "row", "seat"))

    def get_tickets_available(self, obj: MovieSession) -> int:
        hall_capacity = obj.cinema_hall.capacity
        taken = Ticket.objects.filter(movie_session=obj).count()
        return hall_capacity - taken


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["movie_session", "row", "seat"]

    def validate(self, data: dict) -> dict:
        movie_session = data["movie_session"]
        row = data["row"]
        seat = data["seat"]
        hall = movie_session.cinema_hall
        if not (1 <= row <= hall.rows):
            raise serializers.ValidationError({
                "row": f"Row must be between 1 and {hall.rows}"
            })
        if not (1 <= seat <= hall.seats_in_row):
            raise serializers.ValidationError({
                "seat": f"Seat must be between 1 and {hall.seats_in_row}"
            })
        if movie_session.ticket_set.filter(row=row, seat=seat).exists():
            raise serializers.ValidationError({
                "seat": "This seat is already taken for this session."
            })
        return data


class OrderSerializer(serializers.ModelSerializer):
    movie_session = MovieSessionSerializer(
        source="tickets.first.movie_session",
        read_only=True
    )
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "user", "movie_session", "tickets"]
        depth = 1


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ["tickets"]

    def create(self, validated_data: dict) -> Order:
        user = self.context["request"].user
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(user=user)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order
