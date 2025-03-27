from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from hospitalManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('UserManagement.urls')),
    path('api/', include('DiseaseManagement.urls')),

    path('',views.home_view,name=''),

    path('adminclick/', views.adminclick_view,name='adminclick'),
    path('doctorclick/', views.doctorclick_view,name='doctorclick'),
    path('patientclick/', views.patientclick_view,name='patientclick'),

    path('adminsignup/', views.admin_signup_view,name='adminsignup'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),

    path('adminlogin/', views.adminlogin_view,name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='doctorlogin.html'),name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='patientlogin.html'),name='patientlogin'),
    
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    path('doctor-dashboard/', LoginView.as_view(template_name='doctor_dashboard.html'),name='doctor-dashboard'),
    path('patient-dashboard/', LoginView.as_view(template_name='patient_dashboard.html'),name='patient-dashboard'),
    
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('index/', views.index_view,name='index'),
    
]
