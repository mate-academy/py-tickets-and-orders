
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from services.views import (
    UserOrderListView,
    UserOrderCreateView,
    MovieSessionDetailView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/cinema/orders/",
        UserOrderListView.as_view(),
        name="order-list"
    ),
    path(
        "api/cinema/orders/create/",
        UserOrderCreateView.as_view(),
        name="order-create"
    ),
    path(
        "api/cinema/movie_sessions/<int:pk>/",
        MovieSessionDetailView.as_view(),
        name="movie-session-detail"
    ),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
