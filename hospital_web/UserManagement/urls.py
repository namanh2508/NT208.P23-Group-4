from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from UserManagement import views
urlpatterns = [
    path('',views.index_view,name='index_home'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    # check
    path('patientlogin', views.patientlogin_view, name='patientlogin'),
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/<int:doctor_id>/', views.appointment_view, name='appointment_view'),

    path('discharge/',views.GetAllPatientDischargeDetail.as_view(), name="All patient discharge"),
    path('appointment/patient/<str:name>/', views.get_appointment_by_patient_name, name='patient_appointments'),
    path('patient/',views.GetAllPatient.as_view(), name="All-patient"),
    path('all_doctors/', views.all_doctors_view, name='all_doctors'),
    path('my_profile/', views.patient_view_profile, name='my_profile'),
 ]