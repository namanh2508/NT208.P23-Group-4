from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from UserManagement import views
urlpatterns = [
    path('',views.index_view,name='index_home'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    path('patientlogin', views.patientlogin_view, name='patientlogin'),
    path('patient-dashboard', LoginView.as_view(template_name='patient_dashboard.html'), name='patient-dashboard'),
    path('logout/', views.logout_view, name='logout'),
 ]