from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import DoctorSerializer,PatientSerializer,DoctorDetailSerializer
from .serializers import AppointmentSerializer1,AppointmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from hospitalManagement.models import Appointment,Doctor,Patient
from django.http import HttpResponseForbidden
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PatientRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

    



class CreatePatientUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]


class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        try:
            patient = request.user.patient 
        except:
            return Response({"error": "User is not a patient"}, status=400)

        data = request.data.copy()
        data['doctorId'] = doctor.id
        data['patientId'] = patient.id
        data['doctorName'] = doctor.get_name
        data['patientName'] = patient.get_name

        serializer = AppointmentSerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors) 
            return Response(serializer.errors, status=400)

class GetAllDoctor(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    

class GetAllPatient(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
class DoctorDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        serializer = DoctorSerializer(doctor, context={"request": request})
        return Response(serializer.data, status=200)

class GetAppointmentByPatientName(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        name = self.kwargs['name']
        return Appointment.objects.filter(patientId__user__first_name=name)# Lọc theo tên bệnh nhân trong User model


class GetDoctorByName(generics.ListAPIView):
    serializer_class = DoctorDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        name = self.kwargs['name']
        return Doctor.objects.filter(user__first_name=name)  # Lọc theo tên bác sĩ trong User model
def patient_appointments_view(request,patientID):
    patient = get_object_or_404(User, pk=patientID)
    appointments = Appointment.objects.filter(patient_id=patientID).order_by('-appointmentDate')
    if not (request.user.is_staff or request.user.pk == patientID):
        return HttpResponseForbidden("Bạn không có quyền xem lịch hẹn này.")
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, '' , context) # thêm file.html để hiển thị các lịch hẹn của 1 patient
