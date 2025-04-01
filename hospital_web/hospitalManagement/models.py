from django.db import models
from django.contrib.auth.models import User



departments = [
    ('bac_si_tim_mach', 'Bác sĩ Tim mạch'),
    ('bac_si_da_lieu', 'Bác sĩ Da liễu'),
    ('bac_si_cap_cuu', 'Bác sĩ Cấp cứu'),
    ('bac_si_di_ung_mien_dich', 'Bác sĩ Dị ứng/ Miễn dịch'),
    ('bac_si_gay_me', 'Bác sĩ Gây mê'),
    ('bac_si_ngoai_tieu_hoa', 'Bác sĩ Ngoại tiêu hóa')
]
class Admin (models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    full_name= models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    mobile = models.CharField (max_length=11)
    biological_sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    def __str__(self):
        return self.full_name
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, choices=departments, default='bac_si_tim_mach')  # Đổi default
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.last_name + " " +  self.user.first_name 
    @property
    def get_profile_pic(self):
        return self.profile_pic.url if self.profile_pic else None
    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.get_department_display()) 




class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id


class Appointment(models.Model):
    appointmentID=models.AutoField(primary_key=True)
    patientId = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="appointments")  # ForeignKey to Patient
    doctorId = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")  # ForeignKey to Doctor
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(null=True, blank=True)
    appointmentTime=models.TimeField(null=True, blank=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    @property
    def get_patient_name(self):
        return self.patientId.get_name if self.patientId else None
    
     
class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

class Diseases(models.Model):
    diseaseID = models.AutoField(primary_key=True)
    diseaseName = models.CharField(max_length=255, unique=True)
    symptoms = models.TextField() 
    treatment = models.TextField()

class Diagnoses(models.Model):
    diagnosisId = models.AutoField(primary_key=True)
    patientId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_patient")
    doctorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_doctor")
    note = models.TextField(blank=True, null=True)
    
class DiagnosisDisease(models.Model):
    diseaseID = models.ForeignKey(Diseases, on_delete=models.CASCADE)
    diagnosisId = models.ForeignKey(Diagnoses, on_delete=models.CASCADE)
    
