from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('message/', views.msg),

    path("api-token-auth/", obtain_auth_token),

    path('menu/',views.menu,name="menu"),
    path('menu/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/bookings/', views.BookingsView.as_view(), name='Booking_list'),
    path('bookings/', views.bookings, name='bookings'),
    path('custom_404/', views.custom_404, name='custom_404'),
]