from django.shortcuts import render
from rest_framework import generics
from .models import Users
from .models import Appointments
from .serializers import UserSerializer
from .serializers import AppointmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
class AppointmentListView(generics.ListAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)    