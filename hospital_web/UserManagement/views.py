from django.shortcuts import render
from rest_framework import generics
from .models import Users
from .models import Appointments
from .serializers import UserSerializer
from .serializers import AppointmentSerializer
# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
class AppointmentListView(generics.ListAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer