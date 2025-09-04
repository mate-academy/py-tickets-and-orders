from rest_framework import generics, permissions
from django.db.models import QuerySet
from db.models import Order, MovieSession
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    MovieSessionSerializer
)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class UserOrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: OrderCreateSerializer) -> None:
        serializer.save()


class MovieSessionDetailView(generics.RetrieveAPIView):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    permission_classes = [permissions.AllowAny]
