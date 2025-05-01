from django.urls import path
from . import views
from .views import GeminiChatView

urlpatterns = [
   #  path("notes/", views.NoteListCreate.as_view(), name="note-list"),
   #  path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    
   path('appointment/patient/<int:patient_id>/', views.patient_appointments_view, name='patient_appointments'),
   # path("diagnose/", views.DiagnoseView.as_view(), name="diagnose"),
   path("chat/", views.GeminiChatView.as_view(), name='chat'),
   #  path('createuser/', views.CreateUserView.as_view(), name='create-user'),
   #  path('doctor/<str:name>/', views.GetDoctorByName.as_view(), name='doctor_by_name'),
   #  path('doctor/',views.GetAllDoctor.as_view(), name="All-doctor"),
]