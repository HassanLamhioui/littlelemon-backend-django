from django.shortcuts import render
from django.core import serializers
from restaurant.forms import BookingForm
from .models import Booking, Menu
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import BookingSerializer, UserSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    menu_items = Menu.objects.all()
    context = {'menu_items': menu_items}
    return render(request, 'menu.html', context)

def display_menu_item(request, pk):
    menu_item = Menu.objects.filter(pk=pk).first()
    context = {'menu_item': menu_item}
    return render(request, 'menu_item.html', context)

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json})
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin | IsManager]
        return [permission() for permission in permission_classes]

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_permissions(self):
        if self.request.method in ["GET","POST"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin | IsManager]
        return [permission() for permission in permission_classes]

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer