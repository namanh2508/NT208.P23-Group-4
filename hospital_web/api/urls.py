from django.urls import path
from . import views

urlpatterns = [
    
    path('doctor/<str:name>/', views.GetDoctorByName.as_view(), name='doctor_by_name'),
    path('doctor/',views.GetAllDoctor.as_view(), name="All-doctor"),
]