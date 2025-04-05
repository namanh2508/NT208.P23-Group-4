from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

DEPARTMENT= [
    ('bac_si_tim_mach', 'Bác sĩ Tim mạch'),
    ('bac_si_da_lieu', 'Bác sĩ Da liễu'),
    ('bac_si_khoa_noi', 'Bác sĩ Nội Tổng quát'),
    ('bac_si_khoa_ngoai', 'Bác sĩ Ngoại Tổng quát'),
    ('bac_si_di_ung_mien_dich', 'Bác sĩ Dị ứng/ Miễn dịch'),
    ('bac_si_gay_me', 'Bác sĩ Gây mê'),
    ('bac_si_tai_mui_hong', 'Bác sĩ Tai Mũi Họng'),
    ('bac_si_nhi_khoa', 'Bác sĩ Nhi khoa'),
    ('bac_si_phu_san', 'Bác sĩ Phụ sản'),
    ('bac_si_tieu_duong', 'Bác sĩ Tiểu đường'),
    ('bac_si_tieu_hoa', 'Bác sĩ Tiêu hóa'),
    ('bac_si_x_quang', 'Bác sĩ X-quang'),
    ('bac_si_phau_thuat', 'Bác sĩ Phẫu thuật'),
    ('bac_si_tam_ly', 'Bác sĩ Tâm lý'),
    ('bac_si_khoa_hoc', 'Bác sĩ Khoa học'),
    ('bac_si_khoa_khac', 'Bác sĩ Khoa khác')
]

# ---------- Custom User ----------
class CustomUser(AbstractUser):
    picture = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    multi_factor_enabled = models.BooleanField(default=False)
    ip_address_last_login = models.GenericIPAddressField(blank=True, null=True)
    def __str__(self):
        return self.user.get_full_name()

# ---------- Doctor ----------
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True,choices=DEPARTMENT)
    description = models.TextField(blank=True, null=True)
    def get_department(self):
        return dict(DEPARTMENT).get(self.department, 'Unknown')
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

# ---------- Admin ----------
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"Admin {self.user.get_full_name()}"

# ---------- Patient ----------
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    family_phone = models.CharField(max_length=20, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    symptom = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.user.get_full_name()

# ---------- Record ----------
class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='record')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    family_phone = models.CharField(max_length=20, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    symptom = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    record_date = models.DateField()   
    def __str__(self):
        return f"Record for {self.patient} on {self.record_date}"

# ---------- Service ----------
class Service(models.Model):
    record=models.OneToOneField(Record, on_delete=models.CASCADE)
    service_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='service')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='service')
    appointmentDate = models.DateField()
    appointmentTime = models.TimeField()
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"Service #{self.service_id} for {self.patient}"
    
# -------------------- Appointment --------------------
class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointment')
    method = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Appointment for {self.service.patient.user.get_full_name()} with {self.service.doctor.user.get_full_name()}"

# -------------------- Test --------------------
class Test(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='test')
    glucose = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    blood_group = models.CharField(max_length=5)
    men_gan = models.DecimalField(max_digits=5, decimal_places=2)
    cretinine = models.DecimalField(max_digits=5, decimal_places=2)
    acid_uric = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Test for Service #{self.service.service_id}"

# -------------------- Medicine --------------------
class Medicine(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='medicine')
    medicine_name = models.CharField(max_length=100)
    instruction = models.TextField()
    times_per_day = models.CharField(max_length=50)
    effect = models.TextField()
    amount = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine_name} for Service #{self.service.service_id}"

# -------------------- Bill --------------------
class Bill(models.Model):
    service= models.OneToOneField(Service,on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='bill')
    release_date = models.DateField()
    release_time = models.TimeField()
    pay_date = models.DateField(blank=True, null=True)
    pay_time = models.TimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    def __str__(self):
        return f"Bill for {self.patient.user.get_full_name()} on {self.release_date}"




# class Admin (models.Model):
#     user = models.OneToOneField (User, on_delete=models.CASCADE)
# <<<<<<< Updated upstream
#     username= models.CharField(max_length=100)
#     full_name = models.CharField(max_length=100, default="")
# =======
# >>>>>>> Stashed changes
#     email = models.EmailField(unique=True)
#     date_of_birth = models.DateField()
#     mobile = models.CharField (max_length=11)
#     def __str__(self):
#         return self.full_name
# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username= models.CharField(max_length=100)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     date_of_birth = models.DateField()
#     profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20, null=True)
#     biological_sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
#     department = models.CharField(max_length=50, choices=departments, default='bac_si_tim_mach')  # Đổi default
#     status = models.BooleanField(default=False)
#     about = models.TextField(max_length=500, null=True, blank=True)
#     @property
#     def get_name(self):
#         return self.user.last_name + " " +  self.user.first_name 
#     @property
#     def get_profile_pic(self):
#         return self.profile_pic.url if self.profile_pic else None
#     @property
#     def get_id(self):
#         return self.user.id

#     def __str__(self):
#         return "{} ({})".format(self.user.first_name, self.get_department_display()) 




# class Patient(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=False)
#     admitDate=models.DateField(auto_now=True)
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.last_name + " " +  self.user.first_name 
#     @property
#     def get_id(self):
#         return self.user.id


# class Appointment(models.Model):
#     appointmentID=models.AutoField(primary_key=True)
#     patientId = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="appointments")  # ForeignKey to Patient
#     doctorId = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")  # ForeignKey to Doctor
#     patientName=models.CharField(max_length=40,null=True)
#     doctorName=models.CharField(max_length=40,null=True)
#     appointmentDate=models.DateField(null=True, blank=True)
#     appointmentTime=models.TimeField(null=True, blank=True)
#     description=models.TextField(max_length=500)
#     status=models.BooleanField(default=False)
#     @property
#     def get_patient_name(self):
#         return self.patientId.get_name if self.patientId else None
#     @property
#     def get_time(self):
#         return self.appointmentTime.strftime("%H:%M") if self.appointmentTime else None
#     def get_date(self):
#         return self.appointmentDate.strftime("%d/%m/%Y") if self.appointmentDate else None
    
# class timeSlot(models.Model):
#     appointmentID=models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="timeSlots")
#     timeSlot=models.TimeField(null=True, blank=True)
#     status=models.BooleanField(default=False)
#     @property
#     def get_time_slot(self):
#         return self.timeSlot.strftime("%H:%M") if self.timeSlot else None



# class PatientDischargeDetails(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40)
#     assignedDoctorName=models.CharField(max_length=40)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=True)
#     symptoms = models.CharField(max_length=100,null=True)

#     admitDate=models.DateField(null=False)
#     releaseDate=models.DateField(null=False)
#     daySpent=models.PositiveIntegerField(null=False)

#     roomCharge=models.PositiveIntegerField(null=False)
#     medicineCost=models.PositiveIntegerField(null=False)
#     doctorFee=models.PositiveIntegerField(null=False)
#     OtherCharge=models.PositiveIntegerField(null=False)
#     total=models.PositiveIntegerField(null=False)

# class Diseases(models.Model):
#     diseaseID = models.AutoField(primary_key=True)
#     diseaseName = models.CharField(max_length=255, unique=True)
#     symptoms = models.TextField() 
#     treatment = models.TextField()

# class Diagnoses(models.Model):
#     diagnosisId = models.AutoField(primary_key=True)
#     patientId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_patient")
#     doctorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses_as_doctor")
#     note = models.TextField(blank=True, null=True)
    
# class DiagnosisDisease(models.Model):
#     diseaseID = models.ForeignKey(Diseases, on_delete=models.CASCADE)
#     diagnosisId = models.ForeignKey(Diagnoses, on_delete=models.CASCADE)
    
