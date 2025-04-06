from datetime import date, timedelta
from django import forms
from django.contrib.auth.models import User, Group
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator

from .models import Service, Doctor, Patient 
from django.utils import timezone
import datetime

#for signup
class CustomUserSignupForm(forms.ModelForm):
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'}),
        required=True
    )
    confirm_password = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}),
        required=True
    )
    gender = forms.ChoiceField(
        choices=models.GENDER,
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'}),
        label="Giới tính",
        required=True
    )

    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'birthday']
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Họ',
            'last_name': 'Tên',
            'phone': 'Số điện thoại',
            'birthday': 'Ngày sinh',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên đăng nhập'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # 'gender': forms.RadioSelect(choices=models.GENDER),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Mật khẩu xác nhận không khớp!")
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (not phone.isdigit() or len(phone) not in [10, 11]):
            raise forms.ValidationError("Số điện thoại phải là 10 hoặc 11 chữ số và chỉ chứa số.")
        return phone
    # Check if email already exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại. Vui lòng chọn email khác.")
        return email

    # Check if username already exists
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")
        return username
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data["password"])
        user.gender = self.cleaned_data.get("gender")
        if commit:
            user.save()
        return user
    
class AdminSignupForm(CustomUserSignupForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save ()
            models.Admin.objects.create(user=user)
        return user
class DoctorSignupForm(CustomUserSignupForm):
    department = forms.ChoiceField(
        label="Khoa",
        choices=models.DEPARTMENT,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label="Mô tả kinh nghiệm",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập kinh nghiệm làm việc'}),
        required=False
    )

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            models.Doctor.objects.create(
                user=user,
                department=self.cleaned_data["department"],
                description=self.cleaned_data["description"]
            )
        return user
class PatientSignupForm(CustomUserSignupForm):
    family_phone = forms.CharField(
        max_length=11,
        required=True,
        label="Số điện thoại người thân",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại người thân'})
    )
    weight = forms.IntegerField(
        label="Cân nặng (kg)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập cân nặng (kg)'})
    )
    height = forms.IntegerField(
        label="Chiều cao (cm)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập chiều cao (cm)'})
    )
    def clean_family_phone(self):
        family_phone = self.cleaned_data.get('family_phone')
        if family_phone and (not family_phone.isdigit() or len(family_phone) not in [10, 11]):
            raise forms.ValidationError("Số điện thoại người thân phải là 10 hoặc 11 chữ số.")
        return family_phone
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            models.Patient.objects.create(
                user=user,
                family_phone=self.cleaned_data.get('family_phone'),
                weight=self.cleaned_data.get('weight'),
                height=self.cleaned_data.get('height')
            )
        return user

#login form
class LoginForm(forms.ModelForm):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
        required=True
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'}),
        required=True
    )
#for updating profile only
class CustomUserUpdateForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (not phone.isdigit() or len(phone) not in [10, 11]):
            raise forms.ValidationError("Số điện thoại phải hợp lệ (10 hoặc 11 chữ số).")
        return phone
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'birthday',
                  'gender', 'phone', 'picture', 'multi_factor_enabled']
        labels = {
            'first_name': 'Họ',
            'last_name': 'Tên',
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'birthday': 'Ngày sinh',
            'gender': 'Giới tính',
            'phone': 'Số điện thoại',
            'picture': 'Ảnh đại diện',
            'multi_factor_enabled': 'Bật xác thực hai bước',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.RadioSelect(choices=models.GENDER),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'multi_factor_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class AdminDoctorForm(forms.ModelForm): # form để admin quản lý thông tin
    class Meta:
        model = models.Doctor
        fields = ['user', 'department', 'description']
        labels = {
            'user': 'Bác sĩ (tài khoản)',
            'department': 'Khoa',
            'description': 'Mô tả chuyên môn',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(choices=models.DEPARTMENT, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
class AdminPatientForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['user', 'family_phone', 'weight', 'height', 'description']
        labels = {
            'user': 'Người dùng',
            'family_phone': 'Số điện thoại người thân',
            'weight': 'Cân nặng (kg)',
            'height': 'Chiều cao (cm)',
            'description': 'Mô tả triệu chứng',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'family_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
class DoctorUserForm(CustomUserUpdateForm):
    department = forms.ChoiceField(
        choices=models.DEPARTMENT,
        required=False,
        label='Khoa',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        label='Mô tả công việc/Kinh nghiệm',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        # Lấy Doctor từ kwargs
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        # Nếu có trong db, gán dữ liệu cũ
        if doctor:
            self.fields['department'].initial = doctor.department
            self.fields['description'].initial = doctor.description
        self.doctor_instance = doctor  # lưu lại để dùng khi save()
    def save(self, commit=True):
        user = super().save(commit)
        doctor = self.doctor_instance
        if doctor:
            doctor.department = self.cleaned_data.get('department')
            doctor.description = self.cleaned_data.get('description')
            if commit:
                doctor.save()
        return user
class PatientUserForm(CustomUserUpdateForm):
    family_phone = forms.CharField(
        max_length=11,
        required=False,
        label='Số điện thoại người thân',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    weight = forms.IntegerField(
        required=False,
        min_value=0,
        label='Cân nặng (kg)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    height = forms.IntegerField(
        required=False,
        min_value=0,
        label='Chiều cao (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['family_phone'].initial = patient.family_phone
            self.fields['weight'].initial = patient.weight
            self.fields['height'].initial = patient.height
            self.fields['description'].initial = patient.description
        self.patient_instance = patient
    def clean_family_phone(self):
        family_phone = self.cleaned_data.get('family_phone')
        if family_phone and (not family_phone.isdigit() or len(family_phone) not in [10, 11]):
            raise forms.ValidationError("Số điện thoại người thân phải hợp lệ (10 hoặc 11 chữ số).")
        return family_phone

    def save(self, commit=True):
        user = super().save(commit)
        patient = self.patient_instance
        if patient:
            patient.family_phone = self.cleaned_data.get('family_phone')
            patient.weight = self.cleaned_data.get('weight')
            patient.height = self.cleaned_data.get('height')
            patient.description = self.cleaned_data.get('description')
            if commit:
                patient.save()
        return user
        
# class AppointmentForm(forms.ModelForm):
#     # Lấy các ngày hẹn trong vòng 6 ngày
#     available_dates = []
#     today = date.today()
#     for i in range(6):
#         available_dates.append(today + timedelta(days=i))
        
#     appointmentDate = forms.ChoiceField(choices=[(d, d) for d in available_dates], label='Ngày hẹn', widget=forms.RadioSelect)
#     # Lấy các giờ hẹn trong ngày, mỗi 30 phút
#     available_times = [
#         '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
#         '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
#     ]
#     appointmentTime = forms.ChoiceField(choices=[(t, t) for t in available_times], label='Giờ hẹn',  widget=forms.RadioSelect)

#     description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Mô tả triệu chứng...'}))

#     class Meta:
#         model = models.Appointment
#         fields = ['appointmentDate', 'appointmentTime', 'description']
    
    


#for patient related form code cũ
# class PatientUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields = ['first_name', 'last_name', 'username', 'password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
# class PatientForm(forms.ModelForm):
#     class Meta:
#         model=models.Patient
#         fields=['mobile','status', 'profile_pic', 'address']




# class PatientAppointmentForm(forms.ModelForm):
#     doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
#     class Meta:
#         model=models.Appointment
#         fields=['description','status']


# #for contact us page
# class ContactusForm(forms.Form):
#     Name = forms.CharField(max_length=30)
#     Email = forms.EmailField()
#     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


# class AppointmentForm(forms.ModelForm):
#     # Lấy các ngày hẹn trong vòng 6 ngày
#     available_dates = []
#     today = date.today()
#     for i in range(6):
#         available_dates.append(today + timedelta(days=i))
        
#     appointmentDate = forms.ChoiceField(choices=[(d, d) for d in available_dates], label='Ngày hẹn', widget=forms.RadioSelect)
#     # Lấy các giờ hẹn trong ngày, mỗi 30 phút
#     available_times = [
#         '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
#         '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
#     ]
#     appointmentTime = forms.ChoiceField(choices=[(t, t) for t in available_times], label='Giờ hẹn',  widget=forms.RadioSelect)

#     description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Mô tả triệu chứng...'}))

#     class Meta:
#         model = models.Appointment
#         fields = ['appointmentDate', 'appointmentTime', 'description']

# your_app_name/forms.py



class AppointmentBookingForm(forms.ModelForm):
    # Customize the Doctor field to show readable names
    # Use ModelChoiceField to get a dropdown of doctors
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.select_related('user').all(), # Optimize query
        label="Select Doctor",
        empty_label="-- Choose a Doctor --",
        widget=forms.Select(attrs={'class': 'form-control'}) # Add CSS class if using Bootstrap etc.
    )

    # Customize appointmentDate field
    appointmentDate = forms.DateField(
        label="Appointment Date",
        widget=forms.DateInput(
            attrs={
                'type': 'date',       # Use HTML5 date input
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%d') # Prevent selecting past dates
            }
        )
    )

    # Customize appointmentTime field
    appointmentTime = forms.TimeField(
        label="Appointment Time",
        widget=forms.TimeInput(
            attrs={
                'type': 'time',       # Use HTML5 time input
                'class': 'form-control',
                'min': '08:00',      # Example: Clinic opens at 8 AM
                'max': '17:00',      # Example: Clinic closes at 5 PM
                'step': '1800'       # Example: Allow 30-minute intervals (1800 seconds)
            }
        )
    )

    # Customize description field (optional, for patient's notes)
    description = forms.CharField(
        label="Reason for Visit / Symptoms (Optional)",
        required=False, # Make it optional for the patient during booking
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Briefly describe your reason for the appointment or any symptoms you are experiencing.'
            }
        )
    )

    class Meta:
        model = Service
        # Fields the PATIENT needs to fill out when booking
        fields = ['doctor', 'appointmentDate', 'appointmentTime', 'description']
        # Note: 'patient' will be set automatically in the view based on the logged-in user.
        # 'status' will be set to 'pending' automatically.

    def __init__(self, *args, **kwargs):
        # You could potentially pass the user here if needed for filtering doctors, etc.
        # user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # You can add further customizations here if needed
        # Example: Filter doctors based on department passed in kwargs if needed

    # --- Custom Validation (Examples) ---

    def clean_appointmentDate(self):
        """Ensure appointment date is not in the past."""
        date = self.cleaned_data.get('appointmentDate')
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot book an appointment in the past.")
        # Optional: Add validation for weekends/holidays if needed
        # if date and date.weekday() >= 5: # 5 = Saturday, 6 = Sunday
        #     raise forms.ValidationError("Appointments cannot be booked on weekends.")
        return date

    def clean_appointmentTime(self):
        """Ensure appointment time is within allowed hours."""
        time = self.cleaned_data.get('appointmentTime')
        if time:
            # Define allowed time range (adjust as needed)
            min_time = datetime.time(8, 0)  # 8:00 AM
            max_time = datetime.time(17, 0) # 5:00 PM (exclusive if checking strictly, maybe 16:30 is last slot?)

            if not (min_time <= time < max_time):
                 raise forms.ValidationError(f"Appointments can only be booked between {min_time.strftime('%I:%M %p')} and {max_time.strftime('%I:%M %p')}.")
        return time

    def clean(self):
        """
        Check for potential conflicts (e.g., doctor already booked at that time).
        This is a more complex validation requiring database lookups.
        """
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointmentDate')
        appointment_time = cleaned_data.get('appointmentTime')

        # Only proceed if all relevant fields are valid so far
        if doctor and appointment_date and appointment_time:
            # Combine date and time for easier comparison if needed, or check separately
            # Check if another service exists for this doctor at the exact same date and time
            existing_appointments = Service.objects.filter(
                doctor=doctor,
                appointmentDate=appointment_date,
                appointmentTime=appointment_time,
                status__in=['pending', 'accepted'] # Check pending and accepted appointments
            ).exists() # Use exists() for efficiency

            if existing_appointments:
                raise forms.ValidationError(
                    f"Dr. {doctor.user.get_full_name()} is already booked at this date and time. Please choose another slot."
                )

        return cleaned_data
