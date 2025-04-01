from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer,PatientDischargeDetailsSerializer,DoctorSerializer,PatientSerializer,DoctorDetailSerializer
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note
from hospitalManagement.models import Appointment,Doctor,Patient
from hospitalManagement.models import PatientDischargeDetails
from django.http import HttpResponseForbidden
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class GetAllPatientDischargeDetail(generics.ListAPIView):
    queryset = PatientDischargeDetails.objects.all() # Lấy tất cả đối tượng Product
    serializer_class = PatientDischargeDetailsSerializer

class GetAllDoctor(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    
class GetAllPatient(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
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
