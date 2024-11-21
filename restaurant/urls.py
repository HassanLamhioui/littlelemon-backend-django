from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter(trailing_slash=False)
router.register("users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('message/', views.msg),

    path("",include(router.urls)),
    path("api-token-auth/", obtain_auth_token),

    path('menu/',views.menu,name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('bookings/', views.bookings, name='bookings'),
    path('custom_404/', views.custom_404, name='custom_404'),
]