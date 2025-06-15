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
from .serializers import OTPVerifySerializer, PasswordSerializer, Login2FAVerifySerializer, CustomTokenObtainPairSerializer
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
    

# def send_otp_email_for_api(user_email, otp):
#     subject = 'Mã Xác Thực Hai Yếu Tố (2FA) Của Bạn'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     to = [user_email]

#     html_content = render_to_string('otp_2fa_email_template.html', {'otp': otp})
#     text_content = strip_tags(html_content)

#     try:
#         email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
#         email_message.attach_alternative(html_content, "text/html")
#         email_message.send()
        
#     except Exception as e:
#         print(f"Lỗi khi gửi email 2FA: {e}")
#         raise

#--- VIEWS 2FA ---


class UserStatusView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'multi_factor_enabled': request.user.multi_factor_enabled})

# class SendEnableOTPView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user = request.user
#         if user.multi_factor_enabled:
#             return Response({"error": "2FA đã được bật từ trước."}, status=status.HTTP_400_BAD_REQUEST)
        
#         EmailOTP.objects.filter(email=user.email).delete()
#         otp_code = generate_otp()
#         EmailOTP.objects.create(email=user.email, otp=otp_code)
#         try:
#             # send_otp_email_for_api(user.email, otp_code)
#             subject = 'Xác nhận thay đổi bảo mật tài khoản'
#             template = 'otp_2fa_change_template.html' 
#             # send_otp_to_email(user.email, otp_code, subject, template)
#             threading.Thread(target=send_otp_to_email, args=(user.email, otp_code, subject, template), daemon=True).start()
#             return Response({"message": "Một mã OTP đã được gửi đến email của bạn."}, status=status.HTTP_200_OK)
#         except:
#             return Response({"error": "Không thể gửi email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class VerifyAndEnable2FAView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user = request.user
#         serializer = OTPVerifySerializer(data=request.data)
#         if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         otp_code = serializer.validated_data['otp']
#         email_otp = EmailOTP.objects.filter(email=user.email, otp=otp_code).order_by('-created_at').first()
#         if not email_otp:
#             return Response({"error": "Mã OTP không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

#         if email_otp.is_expired():
#             email_otp.delete()
#             return Response({"error": "Mã OTP đã hết hạn."}, status=status.HTTP_400_BAD_REQUEST)
        
#         user.multi_factor_enabled = True
#         user.save()
#         email_otp.delete()
#         return Response({"message": "Xác thực hai yếu tố đã được bật thành công!"}, status=status.HTTP_200_OK)

# class Disable2FAView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user = request.user
#         serializer = PasswordSerializer(data=request.data)
#         if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         password = serializer.validated_data['password']
#         if not user.check_password(password):
#             return Response({"error": "Mật khẩu không chính xác."}, status=status.HTTP_400_BAD_REQUEST)

#         user.multi_factor_enabled = False
#         user.save()
#         EmailOTP.objects.filter(email=user.email).delete() # Dọn dẹp OTP của 2FA
#         return Response({"message": "Xác thực hai yếu tố đã được tắt."}, status=status.HTTP_200_OK)

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
