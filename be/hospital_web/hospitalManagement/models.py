
from django.conf import settings
from django.utils import timezone 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User,Permission,Group
from django.core.validators import FileExtensionValidator
from decimal import Decimal
from django.utils import timezone
import datetime
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
GENDER= [
    ('nam', 'Nam'),
    ('nu','Nữ')
]
STATUS= [
    ('accepted','Accepted'),
    ('rejected','Rejected'),
    ('pending','Pending'),
    ('finished','Finished')
]
APPOINTMENT_METHOD= [
    ('online','Tư vấn online'),
    ('offline','Khám bệnh trực tiếp')
]

TYPE_OF_SERVICE = [
    ('appointment', 'Đăng ký khám bệnh'),
    ('test', 'Xét nghiệm'),
    ('prescription', 'Đặt thuốc'),    
]
# ---------- Custom User ----------
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # Đổi tên để tránh xung đột với auth.User.groups
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_permissions',  # Đổi tên để tránh xung đột
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
    picture = models.ImageField(
    upload_to='profile_pic/',
    default='profile_pic/default.webp',  # Relative to MEDIA_ROOT
    blank=True,
    null=True
    )
    phone = models.CharField(max_length=20, blank=True, null=True) # số điện thoại
    gender = models.CharField(max_length=10, blank=True, null=True,choices=GENDER) # giới tính
    birthday = models.DateField(blank=True, null=True) # ngày sinh
    multi_factor_enabled = models.BooleanField(default=False) # option để bật chức năng 2 factor authentication
    ip_address_last_login = models.GenericIPAddressField(blank=True, null=True) # lưu địa chỉ ip đăng nhập gần nhất cho chức năng 2FA
    status = models.BooleanField(default = True) # tài khoản đã được kích hoạt hay chưa
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email']  
    def __str__(self):
        return self.get_full_name()

# ---------- Doctor ----------
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True,choices=DEPARTMENT) # khoa
    description = models.TextField(blank=True, null=True) # mô tả
    def get_department(self):
        return dict(DEPARTMENT).get(self.department, 'Unknown')
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    @property
    def get_picture(self):
        return self.user.picture.url if self.user.picture else None
    
    @property
    def get_department(self):
        return dict(DEPARTMENT).get(self.department, 'Unknown')

# ---------- Admin ----------
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"Admin {self.user.get_full_name()}"

# ---------- Patient ----------
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    family_phone = models.CharField(max_length=20, blank=True, null=True) # số điện thoại người thân
    weight = models.PositiveIntegerField(blank=True, null=True) # cân nặng
    height = models.PositiveIntegerField(blank=True, null=True) # chiều cao
    description = models.TextField(blank=True, null=True) # mô tả ngoại hình hay gì đó cũng được
    def __str__(self):
        return self.user.get_full_name()
# ---------- Service ----------
class Service(models.Model): 
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='service') # không cho phép xóa tk doctor hay patient khi service chưa hoàn tất
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='service')
    appointmentDate = models.DateField() # ngày hẹn
    appointmentTime = models.TimeField() # thời gian hẹn
    description = models.TextField(blank=True, null=True) # ghi chú của bác sĩ
    type = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_OF_SERVICE)
    status=models.CharField(max_length=10, choices=STATUS, default='pending') # trạng thái đặt hẹn
    image = models.ImageField(upload_to='service_images/', blank=True, null=True) # ảnh chụp dịch vụ
    @property
    def get_type(self):
        return dict(TYPE_OF_SERVICE).get(self.type, 'Unknown')
    

    


# ---------- Record ----------
class Record(models.Model):
    service= models.OneToOneField(Service, on_delete=models.SET_NULL, null=True, blank=True) # 1 bản record sẽ được tạo sau khi khám xong, nếu service bị xóa thì biến này thành null
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='record') # khóa ngoại liên kết với patient
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='record') # khóa ngoại liên kết với doctor
    symptom = models.TextField(blank=True, null=True) # triệu chứng ghi nhận được
    description = models.TextField(blank=True, null=True) # mô tả rõ ràng các loại bệnh chứng khám được
    record_date = models.DateField(blank=True, null=True) # ngày khám 
    def __str__(self):
        return f"Record for {self.patient} on {self.record_date}" 

# -------------------- AI_Record --------------------
class AI_Record (models.Model):
    RECORD_TYPES = (
        ('lab_report', 'Xét nghiệm'),
        ('dermatology', 'Da liễu'),
        ('xray', 'X-quang'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ai_record') # khóa ngoại liên kết với patient
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES, default='lab_report')
    image = models.ImageField(upload_to='ai_inputs/', blank=True, null=True)
    
    # Dùng cho chẩn đoán từ ảnh y học
    diagnosis = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    
    # thông tin khác
    symptom = models.TextField(blank=True, null=True) # triệu chứng ghi nhận được
    description = models.TextField(blank=True, null=True) # mô tả rõ ràng các loại bệnh chứng khám được
    
    created_at = models.DateField(default=timezone.now) # ngày tạo bản ghi
    
    def __str__(self):
        return f"{self.record_type} - {self.patient.name} ({self.record_date})"
    
    class Meta:
        verbose_name = "AI Record"
        verbose_name_plural = "AI Records"


# -------------------- AI Metric lưu chỉ số OCR đc từ ảnh xét nghiệm, thông qua AI phân tích --------------------------------------------- 
class AI_Metric(models.Model):
    ai_record = models.ForeignKey(AI_Record, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=100)  # tên chỉ số
    value = models.FloatField() # giá trị chỉ số
    unit = models.CharField(max_length=20, blank=True, null=True) # đơn vị chỉ số
    reference_range = models.CharField(max_length=100, blank=True, null=True) # khoảng tham chiếu (VD: 4.0-6.0)
    status = models.CharField(max_length=10, blank=True, null=True)  # tình trạng: cao hay thấp hơn bình thường

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit} ({self.status})"
    
    
# -------------------- Appointment --------------------
class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointment')
    method = models.CharField(max_length=100, blank=True, null=True, choices=APPOINTMENT_METHOD) # khám trực tiếp hoặc tư vấn online
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) # giá tiền
    status=models.CharField(max_length=10, choices=STATUS, default='pending') # trạng thái đặt hẹn
    orderCode = models.CharField(max_length=100, blank=True, null=True) # mã đơn hàng
    def __str__(self):
        return f"Appointment for {self.service.patient.user.get_full_name()} with {self.service.doctor.user.get_full_name()}"

# -------------------- Test --------------------
class Test(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Test_date = models.DateField(default=timezone.now) # ngày xét nghiệm

    def __str__(self):
        return f"Test #{self.id} - {self.service.name}"
    
    
# -------------------- Test Parameter lưu chỉ số, cái này do người dùng nhập hoặc là bác sĩ nhập tay , khác với AI_Metric  --------------------
class TestParameter(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=20, blank=True, null=True)
    reference_range = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit} ({self.status})"
    
#--------------------- Upload Test Result --------------------
class UploadTestResult(models.Model):
    TEST_CHOICES = [
        ('blood', 'Máu'),
        ('urine', 'Nước tiểu'),
        ('cancer', 'Ung thư'),
        ('other', 'Khác'),
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='upload_test_results')
    test_type = models.CharField(max_length=20, choices=TEST_CHOICES)
    custom_test_name = models.CharField(max_length=100, blank=True, null=True)
    gpt_result = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='test_results/', blank=True, null=True)
    test_date = models.DateField()
    ocr_text = models.TextField(blank=True, null=True)  # Lưu trữ kết quả OCR từ file
    description = models.TextField(blank=True, null=True)
    test_place = models.CharField(max_length=100, blank=True, null=True)

    def get_display_test_name(self):
        return dict(self.TEST_CHOICES).get(self.test_type) if self.test_type != 'other' else self.custom_test_name

    def __str__(self):
        return f"KQ XN - {self.get_display_test_name()} - {self.patient.user.get_full_name()} ({self.test_date})"
    

# -------------------- Medicine --------------------
class Medicine(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True) # tên thuốc
    brand = models.CharField(max_length=100, blank=True, null=True) # tên công ty sản xuất
    description= models.TextField(blank=True, null=True) # chức năng  thuốc
    times_per_day = models.IntegerField(blank=True, null=True) # uống bao nhiêu lần 1 ngày
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) # giá tiền 1 viên thuốc

# -------------------- Prescription --------------------
class Prescription(models.Model):
    medicine= models.ForeignKey(Medicine, on_delete=models.SET_NULL, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name='prescriptions')
    amount = models.PositiveIntegerField(blank=True, null=True) # số lượng viên thuốc
    total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) # tổng giá tiền
    def get_total_price(self):
        if self.medicine and self.amount:
            return self.medicine.price * self.amount
        return 0  # or None if you prefer
    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)

def __str__(self):
    return f"{self.medicine} for Service #{self.service.id}"

# -------------------- Bill --------------------
class Bill(models.Model):
    service= models.OneToOneField(Service,on_delete=models.SET_NULL, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    release_date = models.DateField(blank=True, null=True) #thời gian xuất đơn
    release_time = models.TimeField(blank=True, null=True)
    pay_date = models.DateField(blank=True, null=True) # thời gian thanh toán
    pay_time = models.TimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) # tổng tiền thanh toán từ TẤT CẢ các dịch vụ con
    status = models.BooleanField(default=False) # Thanh toán rồi hay chưa
    method = models.CharField(max_length=50,blank=True, null=True) # Phương thức thanh toán
    def __str__(self):
        return f"Bill for {self.patient.user.get_full_name()} on {self.release_date}"




    def __str__(self):
        return f"Message from {self.sender.get_full_name()} at {self.timestamp}"
#-------------------- Email OTP ------------------
class EmailOTP (models.Model):
    email = models.EmailField(unique=False, blank=True, null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
    
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)
    
#-------------------- 2FA ------------------    
class TwoFactorAuthOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"2FA OTP for {self.user.username}"

    def is_expired(self):
        # Hết hạn sau 5 phút
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)

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
    
