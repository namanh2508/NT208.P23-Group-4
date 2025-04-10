from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf.urls.static import static

# from api.views import CreateUserView
from hospitalManagement import views
from hospital_web import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('stafflogin/',views.home_view,name='index'),
    path('',views.index_view,name='index_home'),

    path('adminsignup/', views.admin_signup_view,name='adminsignup'),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),

    path('adminlogin/', views.admin_login_view,name='adminlogin'),
    path('doctorlogin/', views.doctor_login_view,name='doctorlogin'),
    path('patientlogin/', views.patient_login_view, name='patientlogin'),
    
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('logout/', views.logout_view, name='logout'),
    #google login
    path('google_login_redirect/', views.google_login_redirect, name='google_login_redirect'),
    path('accounts/google/login/callback/', views.google_callback, name='google_callback'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),
    
    path('accounts/', include('allauth.urls')), #google authentication

    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='aboutus'),
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


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),



    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),

    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),

    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),
    path('book-appointment/', views.book_appointment,name='book-appointment'),
    path('patient-view-appointment/<str:name>', views.get_appointment_by_patient_name, name='patient-view-appointments'),
    path('all_doctors/', views.all_doctors_view, name='all_doctors'),
    
    path('doctor/<int:doctor_id>/', views.Get_Doctor_Detail, name='doctor_detail'),
    path('patient_view_profile/<str:name>', views.GetPatient, name='patient_view_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#url của userManagement cũ
# urlpatterns = [ 
#     path('doctor/<int:doctor_id>/', views.appointment_view, name='appointment_view'),

#     path('discharge/',views.GetAllPatientDischargeDetail.as_view(), name="All patient discharge"),

#     path('patient/',views.GetAllPatient.as_view(), name="All-patient"),

#     path('my_profile/', views.patient_view_profile, name='my_profile'),
#  ]