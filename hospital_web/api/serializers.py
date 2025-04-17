from django.contrib.auth.models import User
from rest_framework import serializers
from hospitalManagement.models import Appointment,Doctor,Patient
from hospitalManagement.models import PatientDischargeDetails
from django.contrib.auth.models import Group
from datetime import datetime

class PatientRegisterSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True)
    mobile = serializers.CharField(write_only=True)
    profile_pic = serializers.ImageField(write_only=True, required=False)

    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "password",
            "first_name", "last_name", "email",
            "address", "mobile", "profile_pic"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        address = validated_data.pop("address")
        mobile = validated_data.pop("mobile")
        profile_pic = validated_data.pop("profile_pic", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
        )

        patient_group, created = Group.objects.get_or_create(name="PATIENT")
        user.groups.add(patient_group)

        Patient.objects.create(
            user=user,
            address=address,
            mobile=mobile,
            profile_pic=profile_pic
        )

        return user

class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()    
    class Meta:
        model = Doctor
        fields = '__all__'
        depth = 1

    def get_full_name(self, obj):
        return obj.get_name
    def get_department(self, obj):
        return obj.get_department_display()

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


class AppointmentSerializer(serializers.ModelSerializer):
    doctorMobile = serializers.SerializerMethodField() 
    doctorDepartment = serializers.SerializerMethodField()
    doctorPicture = serializers.SerializerMethodField()
    class Meta:
        model= Appointment
        fields=["appointmentID","patientName","doctorName","doctorMobile","doctorDepartment", "doctorPicture","appointmentDate"]
    
    def get_doctorMobile(self,obj):
        # Truy cập đối tượng Doctor thông qua doctorId
         return obj.doctorId.mobile if obj.doctorId else None
    
    def get_doctorDepartment(self,obj):
        # Truy cập đối tượng Doctor thông qua doctorId
         return obj.doctorId.department if obj.doctorId else None
     
    def get_doctorPicture(self,obj):
        # Truy cập đối tượng Doctor thông qua doctorId
        return obj.doctorId.profile_pic.url if obj.doctorId.profile_pic else None

class AppointmentSerializer1(serializers.ModelSerializer):
    appointmentTime = serializers.TimeField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def to_internal_value(self, data):
        if 'appointmentTime' in data:
            try:
                data['appointmentTime'] = datetime.strptime(
                    data['appointmentTime'], '%I:%M %p'
                ).time()
            except ValueError:
                try:
                    data['appointmentTime'] = datetime.strptime(
                        data['appointmentTime'], '%I:%M:%S %p'
                    ).time()
                except ValueError:
                    pass 
        return super().to_internal_value(data)

     
class PatientDischargeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDischargeDetails
        fields = '__all__'


    

        

    