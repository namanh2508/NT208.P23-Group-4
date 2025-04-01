from django import forms
from django.contrib.auth.models import User, Group
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


#for signup
class SignupForm(forms.ModelForm):
    user_group = forms.ChoiceField(choices=[
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient')
    ], required=True,
    widget=forms.HiddenInput(attrs={'class': 'hidden-field'}))
    username = forms.CharField(max_length=100,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select your date of birth'}))
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        label="Phone Number",
        validators=[RegexValidator(r'^[0-9]{10,11}$', 'Your phone number is invalid')],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    biological_sex = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True,
        widget=forms.RadioSelect,
        initial='M')
    class Meta:
        model = User
        fields = ['username','email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
        }
    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type', 'Admin')
        super().__init__(*args, **kwargs)
        self.fields['user_group'].initial = form_type

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Mã hóa mật khẩu
        if commit:
            user.save()
            group_name = self.cleaned_data['user_group']
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            profile_data = {
                'user': user,
                'date_of_birth': self.cleaned_data['date_of_birth'],
                'phone_number': self.cleaned_data['phone_number'],
                'biological_sex': self.cleaned_data['biological_sex']
            }
            if group_name == 'Admin':
                models.Admin.objects.create(**profile_data)
            elif group_name == 'Doctor':
                models.Doctor.objects.create(**profile_data)
            elif group_name == 'Patient':
                models.Patient.objects.create(**profile_data)
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
        fields=['phone_number','department','status','profile_pic']



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
        fields=['phone_number','status']



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



