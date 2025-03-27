from django.urls import path
from .views import DiseaseListView
from .views import DiagnoseListView
from .views import DiagnosisDiseaseListView


urlpatterns = [
    path('disease/', DiseaseListView.as_view(), name='user-list'),
    path('diagnose/', DiagnoseListView.as_view(), name='appointment-list'),
    path('diseaseisdiagnose/', DiagnosisDiseaseListView.as_view(), name='appointment-list'),
    

]