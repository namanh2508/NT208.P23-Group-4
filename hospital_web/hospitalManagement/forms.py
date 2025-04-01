from datetime import date, timedelta
from django import forms
from django.contrib.auth.models import User, Group
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from .models import departments


#for signup
class AdminSignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        required=True
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date', 'placeholder': 'Select your date of birth'})
    )
    mobile = forms.CharField(
        max_length=11,
        required=True,
        label="Mobile Number",
        validators=[RegexValidator(r'^[0-9]{10,11}$', 'Phone number must be 10-11 digits')],
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your mobile number'})
    )
    biological_sex = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True,
        widget=forms.RadioSelect,
        initial='M'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            # Tạo profile admin
            admin = models.Admin.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                mobile=self.cleaned_data['mobile'],
                biological_sex=self.cleaned_data['biological_sex']
            )
            # Thêm vào group Admin
            admin_group, created = Group.objects.get_or_create(name='Admin')
            user.groups.add(admin_group)
        
        return user

class DoctorSignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        required=True
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select your date of birth'})
    )
    mobile = forms.CharField(
        max_length=20,
        required=True,
        validators=[RegexValidator(r'^[0-9]{10,11}$', 'Phone number must be 10-11 digits')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'})
    )
    biological_sex = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True,
        widget=forms.RadioSelect,
        initial='M'
    )
    department = forms.ChoiceField(  # Thêm trường department
        choices=departments,  # Sử dụng biến đã import
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),  # Sửa dấu ] thành }
        initial='bac_si_tim_mach'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            # Tạo profile doctor
            doctor = models.Doctor.objects.create(
                user=user,
                mobile=self.cleaned_data['mobile'],
                department=self.cleaned_data['department'],
                # Thêm các trường khác nếu cần
                status=False  # Mặc định chưa được kích hoạt
            )
            # Thêm vào group Doctor
            doctor_group, created = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)
        
        return user
    

#for doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['mobile','department','status','profile_pic']



#for patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    class Meta:
        model=models.Patient
        fields=['mobile','status']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AppointmentForm(forms.ModelForm):
    # Lấy các ngày hẹn trong vòng 6 ngày
    available_dates = []
    today = date.today()
    for i in range(6):
        available_dates.append(today + timedelta(days=i))
        
    appointmentDate = forms.ChoiceField(choices=[(d, d) for d in available_dates], label='Ngày hẹn')

    # Lấy các giờ hẹn trong ngày, mỗi 30 phút
    available_times = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ]
    appointmentTime = forms.ChoiceField(choices=[(t, t) for t in available_times], label='Giờ hẹn')

    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Mô tả triệu chứng...'}))

    class Meta:
        model = models.Appointment
        fields = ['appointmentDate', 'appointmentTime', 'description']
