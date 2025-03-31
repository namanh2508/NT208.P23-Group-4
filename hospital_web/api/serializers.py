from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note
from hospitalManagement.models import Appointment,Doctor
from hospitalManagement.models import PatientDischargeDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields='__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Appointment
        fields=["appointmentID","patientName","patientName", "appointmentDate", "status"]
    
    
class PatientDischargeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDischargeDetails
        fields = '__all__'
        

    

        

    