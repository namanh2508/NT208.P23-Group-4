from rest_framework import serializers
from .models import Diseases
from .models import Diagnoses
from .models import DiagnosisDisease

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseases
        fields = '__all__'
        
class DiagnoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnoses
        fields = '__all__' 
        
class DiagnosisDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisDisease
        fields = '__all__' 