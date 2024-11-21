from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated
from restaurant.forms import BookingForm
from .models import Booking, Menu
from .serializers import BookingSerializer, UserSerializer, MenuSerializer
from .permissions import IsAdmin, IsManager
from datetime import datetime
import json

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
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'reservations.html', {"bookings": booking_json})

def custom_404(request):
    return render(request, 'custom_404.html')

class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
class BookingsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

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

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        try:
            # Load and validate JSON data
            data = json.loads(request.body)
            required_fields = ['first_name', 'reservation_date', 'reservation_slot', 'guest_number']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f"Missing field: {field}"}, status=400)

            # Check if the booking exists
            reservation_date = parse_date(data['reservation_date'])
            if reservation_date is None:
                return JsonResponse({'error': 'Invalid reservation_date format'}, status=400)

            exist = Booking.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=data['reservation_slot']
            ).exists()

            if not exist:
                # Save new booking
                booking = Booking(
                    first_name=data['first_name'],
                    guest_number=data['guest_number'],
                    reservation_date=reservation_date,
                    reservation_slot=data['reservation_slot'],
                )
                booking.save()
                return JsonResponse({'success': True, 'booking_id': booking.id}, status=201)
            else:
                return JsonResponse({'error': 'Slot already booked'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)

    if request.method == 'GET':
        # Validate and parse the 'date' parameter
        date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        reservation_date = parse_date(date_str)
        if reservation_date is None:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Retrieve and serialize bookings for the given date
        bookings = Booking.objects.filter(reservation_date=reservation_date)
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')

    # If method not allowed
    return JsonResponse({'error': 'Method not allowed'}, status=405)
@api_view()
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def msg(request):
    return Response({"message":"This view is protected"})