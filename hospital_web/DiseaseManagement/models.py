from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model() # sử dụng cái model Users trong UserManagement
class Diseases(models.Model):
    diseaseID = models.AutoField(primary_key=True)
    diseaseName = models.CharField(max_length=255, unique=True)
    symptoms = models.JSONField()  # Lưu danh sách triệu chứng dạng JSON
    treatment = models.TextField()

class Diagnoses(models.Model):
    diagnosisId = models.AutoField(primary_key=True)
    patientId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_patient")
    doctorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_doctor")
    note = models.TextField(blank=True, null=True)
    
class DiagnosisDisease(models.Model):
    diseaseID = models.ForeignKey(Diseases, on_delete=models.CASCADE)
    diagnosisId = models.ForeignKey(Diagnoses, on_delete=models.CASCADE)
     
    