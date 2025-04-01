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
 ]