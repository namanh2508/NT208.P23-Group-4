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
import requests

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


# def show_disease_diagnose(request):
#     disease_response = requests.get("api/disease")
#     diagnose_response = requests.get("api/diagnose")
#     if disease_response.status_code == 200 and diagnose_response.status_code == 200:
#         diseases = disease_response.json()        
#         diagnoses = diagnose_response.json() 
#     else:
#         diseases=[]
#         diagnoses=[]
#     context= {
#         'diagnoses' : diagnoses,
#         'diseases' : diseases
#     }       
#     return render(request, 'test.html', context)