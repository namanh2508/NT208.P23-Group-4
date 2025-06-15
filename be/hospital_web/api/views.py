from django.shortcuts import render,get_object_or_404
from requests import models
from django.contrib.auth.models import User
from rest_framework import generics
import hospitalManagement.models
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import *
from .serializers import AppointmentBookingSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
import google.generativeai as genai
from django.views.generic import TemplateView
from hospitalManagement.models import CustomUser,Doctor
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .serializers import OTPVerifySerializer, PasswordSerializer, Login2FAVerifySerializer
from hospitalManagement.views import generate_otp
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from hospitalManagement.models import CustomUser, EmailOTP
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import SessionAuthentication
from hospitalManagement.models import CustomUser, Doctor, Patient, EmailOTP
from hospitalManagement.views import send_otp_to_email
import threading


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

genai.configure(api_key="AIzaSyDqT2XW78e3x_X4lKgXSgAzJEIdA64LUfE")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

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
        
class CreatePatientUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]

class GetAllDoctor(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    def get_serializer_context(self):
        return {'request': self.request}

class DoctorDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        serializer = DoctorSerializer(doctor, context={"request": request})
        return Response(serializer.data, status=200)

class BookAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doctor_id):
        try:
            patient = request.user.patient
        except:
            return Response({"error": "Bạn chưa có thông tin hồ sơ bệnh nhân."}, status=400)

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Không tìm thấy bác sĩ."}, status=404)

        serializer = AppointmentBookingSerializer(data=request.data, context={'request': request, 'doctor_id': doctor_id})
        if serializer.is_valid():
            service = serializer.save()
            return Response({
                "message": "Đặt lịch thành công.",
                "service_id": service.id
            }, status=201)
        else:
            return Response(serializer.errors, status=400)

class PatientProfileAPIView(RetrieveAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Patient.objects.get(user=self.request.user)
    

#--- VIEWS 2FA ---


class UserStatusView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'multi_factor_enabled': request.user.multi_factor_enabled})

class Toggle2FAView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        password = serializer.validated_data['password']
        if not user.check_password(password):
            return Response({"error": "Mật khẩu không chính xác."}, status=status.HTTP_400_BAD_REQUEST)

        # Đảo ngược trạng thái 2FA
        user.multi_factor_enabled = not user.multi_factor_enabled
        user.save()

        if user.multi_factor_enabled:
            message = "Xác thực hai yếu tố đã được bật thành công."
        else:
            message = "Xác thực hai yếu tố đã được tắt."
            # Dọn dẹp OTP cũ nếu có
            EmailOTP.objects.filter(email=user.email).delete()

        return Response({"message": message, "is_enabled": user.multi_factor_enabled})
