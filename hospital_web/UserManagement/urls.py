from django.urls import path
from .views import UserListView
from .views import AppointmentListView
urlpatterns = [
    path('user/', UserListView.as_view(), name='user-list'),
    path('appointment/', AppointmentListView.as_view(), name='appointment-list'),
]