from django.shortcuts import render
from rest_framework import generics
from .models import Diseases
from .models import Diagnoses
from .models import DiagnosisDisease
from .serializers import DiseaseSerializer
from .serializers import DiagnoseSerializer
from .serializers import DiagnosisDiseaseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
class DiseaseListView(generics.ListAPIView):
    queryset = Diseases.objects.all()
    serializer_class = DiseaseSerializer
    
class DiagnoseListView(generics.ListAPIView):
    queryset = Diagnoses.objects.all()
    serializer_class = DiagnoseSerializer
    
class DiagnosisDiseaseListView(generics.ListAPIView):
    queryset = DiagnosisDisease.objects.all()
    serializer_class = DiagnosisDiseaseSerializer
    