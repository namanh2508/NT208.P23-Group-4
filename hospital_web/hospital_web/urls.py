from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from api.views import CreateUserView
from hospitalManagement import views
urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('IV-Medical/', include('UserManagement.urls')),

    path('',views.home_view,name='index'),

 #   path('patientsignup/', views.patient_signup_view,name='patientsignup'),
=======
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),

    path('api/', include('UserManagement.urls')),
    path('api/', include('DiseaseManagement.urls')),

    path('',views.home_view,name=''),
    path('adminclick/', views.adminclick_view,name='adminclick'),
    path('doctorclick/', views.doctorclick_view,name='doctorclick'),
    path('patientclick/', views.patientclick_view,name='patientclick'),

    path('adminsignup/', views.admin_signup_view,name='adminsignup'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),
>>>>>>> df227b7bbecd7cf084fed941d3274200dbb18ac9

    path('adminlogin/', views.adminlogin_view,name='adminlogin'),
    path('stafflogin/', views.doctorlogin_view,name='adminlogin'),
    
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),
    
    path('doctor-dashboard/', LoginView.as_view(template_name='doctor_dashboard.html'),name='doctor-dashboard'),
    
    path('accounts/', include('allauth.urls')), #google authentication


    # --------------------for admin dasboard:--------------------
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    #----------------------thanh doctor--------------------------
    #nút 1
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),

    #nút 2
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),

    #nút 3
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),

    #nút 4
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),

    #----------------------thanh patient--------------------------
    #nút 1
    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    #nút 2
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    #nút 3
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    #nút 4
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

]
