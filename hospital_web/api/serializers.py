from django.contrib.auth.models import User,Group, Permission
from rest_framework import serializers
# from .models import Note
from hospitalManagement.models import Appointment,Doctor,Patient,CustomUser,Admin
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

    