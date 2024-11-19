from rest_framework import serializers
from .models import Booking, Menu
from django.contrib.auth.models import User

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "guest_number":{"min_value":1},
        }

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        extra_kwargs = {
            "price":{"min_value":1},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'groups']
        fields = ["id", "username", "password", "email", "first_name", "last_name", "is_active", "is_staff", "groups", "url"]