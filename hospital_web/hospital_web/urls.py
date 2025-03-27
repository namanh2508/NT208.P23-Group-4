"""
URL configuration for hospital_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from hospitalManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('UserManagement.urls')),
    path('api/', include('DiseaseManagement.urls')),
    path('',views.home_view,name=''),
    # path('test/',views.admin_dashboard),
    path('adminclick/', views.adminclick_view,name='adminclick'),
    path('doctorclick/', views.doctorclick_view,name='doctorclick'),
    path('patientclick/', views.patientclick_view,name='patientclick'),

    path('adminsignup/', views.admin_signup_view,name='adminsignup'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),

    path('adminlogin/', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='doctorlogin.html'),name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='patientlogin.html'),name='patientlogin'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('admin-dashboard/', LoginView.as_view(template_name='admin_dashboard.html'),name='admin-dashboard'),
    path('doctor-dashboard/', LoginView.as_view(template_name='doctor_dashboard.html'),name='doctor-dashboard'),
    path('patient-dashboard/', LoginView.as_view(template_name='patient_dashboard.html'),name='patient-dashboard'),
    path('aboutus/', LoginView.as_view(template_name='aboutus.html'), name='aboutus'),
    path('index/', LoginView.as_view(template_name='index.html'),name='index'),
    path('contactus/', LoginView.as_view(template_name='contactus.html'),name='contactus'),
    path('logout/', views.logout_view, name='logout'),
    
]
