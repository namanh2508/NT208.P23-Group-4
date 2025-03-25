from django.db import models

# Create your models here.
class Users(models.Model):
    BIOLOGICAL_SEX_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )
    ROLE_CHOICES = (
        (0, 'Patient'),
        (1, 'Doctor'),
        (2, 'Admin'),
    )
    userID = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    biological_sex = models.IntegerField(choices=BIOLOGICAL_SEX_CHOICES)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    specialty = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs): 
        if self.role != 1:  # Nếu không phải Doctor
            self.specialty = None  # Xóa giá trị specialty (để đảm bảo chỉ Doctor mới có)
        super().save(*args, **kwargs) # gọi super để biết đc đây là method save() của Django
    
    USERNAME_FIELD = 'email' # đăng nhập hệ thống bằng email thay vì username mặc định của Django
    REQUIRED_FIELDS = [] # ko cần bắt buộc thêm field khác để đăng nhập ( username và password là đủ)


class Appointments(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('no_show', 'No Show'),
    ]
    patientID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="appointment_of_patient")
    doctorID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="appointment_of_doctor")
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    def __str__(self):
        return f"Appointment {self.id} - {self.patient.name} with Dr. {self.doctor.name} on {self.appointment_date}"