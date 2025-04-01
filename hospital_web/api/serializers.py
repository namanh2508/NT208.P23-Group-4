from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note
from hospitalManagement.models import Appointment,Doctor,Patient
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
        depth = 1 
class DoctorDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields=['first_name','last_name','mobile','department','profile_pic']
        depth = 1
    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name
    
    
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields='__all__'
        depth = 1

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}
class AppointmentSerializer(serializers.ModelSerializer):
    doctorMobile = serializers.SerializerMethodField() 
    doctorDepartment = serializers.SerializerMethodField()
    class Meta:
        model= Appointment
        fields=["appointmentID","patientName","doctorName","doctorMobile","doctorDepartment", "appointmentDate"]
    
    def get_doctorMobile(self,obj):
        # Truy cập đối tượng Doctor thông qua doctorId
         return obj.doctorId.mobile if obj.doctorId else None
    
    def get_doctorDepartment(self,obj):
        # Truy cập đối tượng Doctor thông qua doctorId
         return obj.doctorId.department if obj.doctorId else None
     
     
     
class PatientDischargeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDischargeDetails
        fields = '__all__'
        

    

        

    