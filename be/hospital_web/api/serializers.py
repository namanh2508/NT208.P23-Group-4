from django.contrib.auth.models import User,Group, Permission
from rest_framework import serializers
# from .models import Note
from hospitalManagement.models import Appointment,Doctor,Patient,CustomUser,Admin
from datetime import datetime
from hospitalManagement.models import Service, Appointment, Test
from hospitalManagement.models import TwoFactorAuthOTP
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
# from hospitalManagement.models import PatientDischargeDetails


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "password"]
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         print(validated_data)
#         user = User.objects.create_user(**validated_data)
#         return user

# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields='__all__'
#         depth = 1 
# class DoctorDetailSerializer(serializers.ModelSerializer):
#     first_name = serializers.SerializerMethodField()
#     last_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Doctor
#         fields=['first_name','last_name','mobile','department','profile_pic']
#         depth = 1
#     def get_first_name(self, obj):
#         return obj.user.first_name

#     def get_last_name(self, obj):
#         return obj.user.last_name
    
    
# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields='__all__'
#         depth = 1

# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Note
#         fields = ["id", "title", "content", "created_at", "author"]
#         extra_kwargs = {"author": {"read_only": True}}
# class AppointmentSerializer(serializers.ModelSerializer):
#     doctorMobile = serializers.SerializerMethodField() 
#     doctorDepartment = serializers.SerializerMethodField()
#     doctorPicture = serializers.SerializerMethodField()
#     class Meta:
#         model= Appointment
#         fields=["appointmentID","patientName","doctorName","doctorMobile","doctorDepartment", "doctorPicture","appointmentDate"]
    
#     def get_doctorMobile(self,obj):
#         # Truy cập đối tượng Doctor thông qua doctorId
#          return obj.doctorId.mobile if obj.doctorId else None
    
#     def get_doctorDepartment(self,obj):
#         # Truy cập đối tượng Doctor thông qua doctorId
#          return obj.doctorId.department if obj.doctorId else None
     
#     def get_doctorPicture(self,obj):
#         # Truy cập đối tượng Doctor thông qua doctorId
#         return obj.doctorId.profile_pic.url if obj.doctorId.profile_pic else None
     
     
     
# class PatientDischargeDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientDischargeDetails
#         fields = '__all__'




# -------------------------------------------API mới------------------------------------------------------

DEPARTMENT = [
    ('Cardiology', 'Cardiology'),
    ('Neurology', 'Neurology'),
    ('Pediatrics', 'Pediatrics'),
    ('Orthopedics', 'Orthopedics'),
    ('Dermatology', 'Dermatology'),
    ('Radiology', 'Radiology'),
    ('Psychiatry', 'Psychiatry'),
    ('General Medicine', 'General Medicine'),
    ('Surgery', 'Surgery'),
    ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
    ('Ophthalmology', 'Ophthalmology'),
    ('ENT', 'ENT'),
    ('Gastroenterology', 'Gastroenterology'),
    ('Urology', 'Urology'),
    ('Oncology', 'Oncology'),
    ('Endocrinology', 'Endocrinology'),
]

# API này cho biết user đó thuộc nhóm nào
# sử dụng cho CustomUsserSerializer
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

# API này cho biết user đó có quyền gì
# sử dụng cho CustomUsserSerializer
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')

# API cho phép hiện thị thông tin các nhân của user
# và cho phép tạo/cập nhật user với thông tin cá nhân
class CustomUserSerializer(serializers.ModelSerializer):
    
    groups = GroupSerializer(many=True, read_only=True) 
    user_permissions = PermissionSerializer(many=True, read_only=True) 

    class Meta:
        model = CustomUser
        # Liệt kê các trường sẽ hiển thị/chỉnh sửa qua API
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'picture', 'phone', 'gender', 'birthday',
            'multi_factor_enabled', 'ip_address_last_login',
            'is_active', 'is_staff', 'date_joined',
            'groups', 'user_permissions'
            
        )
        read_only_fields = ('ip_address_last_login', 'date_joined', 'is_staff') # Các trường chỉ đọc


    # API để cập nhật thông tin cá nhân của user
    
    # Nếu  muốn cho phép tạo/cập nhật user với password:
    # Cần thêm 'password' vào fields và extra_kwargs
    # extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}
    # Và override phương thức create/update để hash password
    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(**validated_data) # Dùng create_user để hash password
    #     return user
    #
    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password', None)
    #     user = super().update(instance, validated_data)
    #     if password:
    #         user.set_password(password)
    #         user.save()
    #     return user

# API hiện thị thông tin chi tiết của bác sĩ
# và cho phép tạo/cập nhật bác sĩ với thông tin user
class DoctorSerializer(serializers.ModelSerializer):
    # Hiển thị chi tiết user thay vì chỉ ID
    user = CustomUserSerializer(read_only=True) # Chỉ đọc thông tin user khi lấy Doctor
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    ) # Cho phép gán user bằng ID khi tạo/cập nhật Doctor
    department_display = serializers.CharField(source='get_department', read_only=True) # Hiển thị tên khoa

    class Meta:
        model = Doctor
        fields = ('id', 'user', 'user_id', 'department', 'department_display', 'description')
       

# API hiện thị thông tin chi tiết của admin
# và cho phép cập nhật Admin với thông tin user
class AdminSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Admin
        fields = ('id', 'user', 'user_id')



# hỗ trợ hiển thị tên đầy đủ thông tin cho bệnh nhân
# và cho phép tạo/cập nhật bệnh nhân với thông tin user
class PatientSerializer(serializers.ModelSerializer):
    # Cho phép user là null nên cần required=False
    user = CustomUserSerializer(read_only=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True, allow_null=True, required=False
    )
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True, allow_null=True) # Hiển thị tên đầy đủ

    class Meta:
        model = Patient
        fields = (
            'id', 'user', 'user_id', 'user_full_name', 'family_phone',
            'weight', 'height', 'symptom', 'description', 'picture'
        )    

#API người dùng nhập triệu chứng chuẩn đoán, chatgpt trả lời
class SymptomSerializer(serializers.Serializer):
    symptoms = serializers.CharField()

class PatientRegisterSerializer(serializers.ModelSerializer):
    family_phone = serializers.CharField(required=False, allow_blank=True)
    weight = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=CustomUser._meta.get_field('gender').choices, required=False)
    birthday = serializers.DateField(required=False)
    picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'phone', 'gender', 'birthday', 'picture',
            'family_phone', 'weight', 'height', 'description',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        patient_data = {
            'family_phone': validated_data.pop('family_phone', None),
            'weight': validated_data.pop('weight', None),
            'height': validated_data.pop('height', None),
            'description': validated_data.pop('description', None),
        }

        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        patient_group, _ = Group.objects.get_or_create(name="PATIENT")
        user.groups.add(patient_group)

        Patient.objects.create(user=user, **patient_data)

        return user
    
class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'department','picture']

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_department(self, obj):
        return obj.get_department
    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.user.picture and request:
            return request.build_absolute_uri(obj.user.picture.url)  
        return None
    
APPOINTMENT_METHOD= [
    ('online','Tư vấn online'),
    ('offline','Khám bệnh trực tiếp')
]
TYPE_OF_SERVICE = [
    ('appointment', 'Đăng ký khám bệnh'),
    ('test', 'Xét nghiệm'),   
]
class AppointmentBookingSerializer(serializers.Serializer):
    appointmentDate = serializers.DateField()
    appointmentTime = serializers.TimeField()
    description = serializers.CharField(required=False, allow_blank=True)
    type = serializers.ChoiceField(choices=TYPE_OF_SERVICE)
    method = serializers.ChoiceField(choices=APPOINTMENT_METHOD)

    def create(self, validated_data):
        request = self.context['request']
        patient = request.user.patient
        doctor_id = self.context['doctor_id']
        doctor = Doctor.objects.get(id=doctor_id)

        service = Service.objects.create(
            patient=patient,
            doctor=doctor,
            appointmentDate=validated_data['appointmentDate'],
            appointmentTime=validated_data['appointmentTime'],
            description=validated_data.get('description', ''),
            type=validated_data.get('type', ''),
            status='pending'
        )

        if validated_data['type'] == 'appointment':
            Appointment.objects.create(
                service=service,
                method=validated_data['method'],
                status='pending'
            )
        elif validated_data['type'] == 'test':
            Test.objects.create(
                service=service,
                Test_date=validated_data['appointmentDate']  # hoặc timezone.now() nếu không muốn dùng ngày hẹn
            )

        return service
    
class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone', allow_null=True)
    gender = serializers.CharField(source='user.gender', allow_null=True)
    birthday = serializers.DateField(source='user.birthday', allow_null=True)
    picture = serializers.ImageField(source='user.picture', allow_null=True)

    class Meta:
        model = Patient
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'gender', 'birthday', 'picture',
            'family_phone', 'weight', 'height', 'description'
        ]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        
        if user.is_two_factor_enabled:
            otp = self.context['request'].data.get('otp')

            if not otp:
                raise AuthenticationFailed(
                    {"message": "Mã OTP là bắt buộc.", "2fa_required": True}, 
                    code='2fa_required'
                )
            
            try:
                two_factor_otp = TwoFactorAuthOTP.objects.get(user=user, otp=otp)
                
                if two_factor_otp.is_expired():
                    raise AuthenticationFailed(
                        {"message": "Mã OTP đã hết hạn."},
                        code='2fa_expired'
                    )
                
                two_factor_otp.delete()

            except TwoFactorAuthOTP.DoesNotExist:
                raise AuthenticationFailed(
                    {"message": "Mã OTP không hợp lệ."},
                    code='2fa_invalid'
                )
        
        return data
    
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=6, min_length=6)

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, style={'input_type': 'password'})

class Login2FAVerifySerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, max_length=6, min_length=6)