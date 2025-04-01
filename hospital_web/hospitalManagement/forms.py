from datetime import date, timedelta
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import AuthenticationForm


#for signup
class SignupForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    biological_sex = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=True)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Mã hóa mật khẩu
        if commit:
            user.save()
            SignupForm.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                phone_number=self.cleaned_data['phone_number'],
                sex=self.cleaned_data['sex'],
                speciality=self.cleaned_data['speciality']
            )
        return user
    
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
#for doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']



#for patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    class Meta:
        model=models.Patient
        fields=['address','mobile','status']



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
