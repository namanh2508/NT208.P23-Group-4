from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path('discharge/',views.GetAllPatientDischargeDetail.as_view(), name="All patient discharge"),
    path('appointment/patient/<str:name>/', views.GetAppointmentByPatientName.as_view(), name='patient_appointments'),
    path('doctor/',views.GetAllDoctor.as_view(), name="All-doctor"),
    path('patient/',views.GetAllPatient.as_view(), name="All-patient"),
    # path('appointment/patient/<int:patient_id>/', views.patient_appointments_view, name='patient_appointments'),
    path('createuser/', views.CreateUserView.as_view(), name='create-user'),
    path('doctor/<str:name>/', views.GetDoctorByName.as_view(), name='doctor_by_name'),
]