from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views


router = DefaultRouter(trailing_slash=False)
router.register("users", views.UserViewSet, basename="user")

urlpatterns = [
    path("",include(router.urls)),
    path("home/", views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),

    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_auth_token),

    path('menu/',views.menu,name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('bookings/', views.bookings, name='bookings'),
]

