from django.urls import path
from .views import UserListView
from .views import AppointmentListView
from .views import create_user

urlpatterns = [
    path('user/', UserListView.as_view(), name='user-list'),
    path('appointment/', AppointmentListView.as_view(), name='appointment-list'),
    path('create-user/', create_user, name="create-user"),

]