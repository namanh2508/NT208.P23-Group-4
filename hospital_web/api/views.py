from django.shortcuts import render,get_object_or_404
from requests import models
import hospitalManagement.models
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
# from .serializers import SymptomSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
import google.generativeai as genai
from django.views.generic import TemplateView
# from django.contrib.auth.models import User
# from rest_framework import generics
# from .serializers import UserSerializer, NoteSerializer,PatientDischargeDetailsSerializer,DoctorSerializer,PatientSerializer,DoctorDetailSerializer
# from .serializers import AppointmentSerializer
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from .models import Note
# from hospitalManagement.models import Appointment,Doctor,Patient
# from hospitalManagement.models import PatientDischargeDetails

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response


# class NoteListCreate(generics.ListCreateAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         user = self.request.user
#         return Note.objects.filter(author=user)

#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             serializer.save(author=self.request.user)
#         else:
#             print(serializer.errors)


# class NoteDelete(generics.DestroyAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         user = self.request.user
#         return Note.objects.filter(author=user)


# class CreateUserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class GetAllPatientDischargeDetail(generics.ListAPIView):
#     queryset = PatientDischargeDetails.objects.all() # Lấy tất cả đối tượng Product
#     serializer_class = PatientDischargeDetailsSerializer

# class GetAllDoctor(generics.ListAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = [AllowAny]
    
# class GetAllPatient(generics.ListAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [AllowAny]
    
# class GetAppointmentByPatientName(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         name = self.kwargs['name']
#         return Appointment.objects.filter(patientId__user__first_name=name)# Lọc theo tên bệnh nhân trong User model


# class GetDoctorByName(generics.ListAPIView):
#     serializer_class = DoctorDetailSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         name = self.kwargs['name']
#         return Doctor.objects.filter(user__first_name=name)  # Lọc theo tên bác sĩ trong User model
def patient_appointments_view(request,patientID):
    patient = get_object_or_404(models.Patient, pk=patientID)
    if not (request.user.is_staff or request.user == patient.user):
        return HttpResponseForbidden("Bạn không có quyền xem lịch hẹn này.")
    appointments = models.Appointment.objects.filter(patient=patient).order_by('-appointmentDate')
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, '' , context) # thêm file.html để hiển thị các lịch hẹn của 1 patient

genai.configure(api_key="AIzaSyCyJiVy8beS2XiDEBz7vosPP5Sh65yp5zU")

# Use the correct model and v1-compatible method
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

class GeminiChatView(APIView):
    def post(self, request):
        message = request.data.get("message", "")
        if not message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Pass message as a list
            response = model.generate_content([message])
            text_reply = getattr(response, 'text', 'No response text available')

            return Response({"reply": text_reply})
        except Exception as e:
            return Response({"error": "Gemini API error", "details": str(e)}, status=500)
        
class ChatPageView(TemplateView):
    template_name = "chatbot.html"