from django.urls import path
from . import views
from .views import GeminiChatView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
   #  path("notes/", views.NoteListCreate.as_view(), name="note-list"),
   #  path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    
   path('appointment/patient/<int:patient_id>/', views.patient_appointments_view, name='patient_appointments'),
   # path("diagnose/", views.DiagnoseView.as_view(), name="diagnose"),
   path("chat/", views.GeminiChatView.as_view(), name='chat'),
   #  path('createuser/', views.CreateUserView.as_view(), name='create-user'),
   #  path('doctor/<str:name>/', views.GetDoctorByName.as_view(), name='doctor_by_name'),
   #  path('doctor/',views.GetAllDoctor.as_view(), name="All-doctor"),


#    path("patient/register/", views.CreatePatientUserView.as_view(), name="register"),
#    path('doctors/', views.GetAllDoctor.as_view(), name='doctor-list'),
#    path('doctors/<int:doctor_id>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
#    path('book-appointment/<int:doctor_id>/', views.BookAppointmentAPIView.as_view(), name='api-book-appointment'),
#    path('patient/profile/', views.PatientProfileAPIView.as_view(), name='patient-profile'),
#    path("chat/", views.GeminiChatView.as_view(), name='chat'),
#    path('appointment/patient/<int:patient_id>/', views.patient_appointments_view, name='patient_appointments'),

#    # path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh_api'),
#    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
# #    # path('token/verify-2fa/', views.VerifyLoginOTPView.as_view(), name='token_verify_2fa'),
#    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),


    path('2fa/status/', views.UserStatusView.as_view(), name='2fa-status'),
    path('2fa/toggle/', views.Toggle2FAView.as_view(), name='2fa-toggle'),
    # path('2fa/enable/send-otp/', views.SendEnableOTPView.as_view(), name='2fa-send-otp'),
    # path('2fa/enable/verify/', views.VerifyAndEnable2FAView.as_view(), name='2fa-verify-otp'),
    # path('2fa/disable/', views.Disable2FAView.as_view(), name='2fa-disable'),

]