from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from hospitalManagement import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from hospitalManagement.models import Doctor  # Import the Doctor model
from api.serializers import PatientDischargeDetailsSerializer,DoctorSerializer,PatientSerializer
from api.serializers import AppointmentSerializer
from hospitalManagement.models import Appointment,Doctor,Patient
from hospitalManagement.models import PatientDischargeDetails
# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    doctors = Doctor.objects.all()
    return render(request, 'index_home.html', {'doctors': doctors})

def all_doctors_view(request):
    doctors = Doctor.objects.all()  # Lấy tất cả bác sĩ từ database
    return render(request, 'all_doctors.html', {'doctors': doctors})

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return redirect('patientlogin')
    return render(request,'patientsignup.html',context=mydict)

def patientlogin_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Django�s built-in login form
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="PATIENT").exists():
                login(request, user)
                return redirect("patient-dashboard")
            else:
                form.add_error(None, "Không tìm thấy tài khoản của bạn")

    else:
        form = AuthenticationForm()

    return render(request, "patientlogin.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('index_home')

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    if request.user.is_authenticated:
        doctors = Doctor.objects.all() 
        return render(request, 'patient_dashboard.html', {'doctors': doctors})
    else:
        return redirect('patientlogin')

@login_required(login_url='/IV-Medical/patientsignup')
def appointment_view(request, doctor_id):
    # Lấy thông tin bác sĩ từ doctor_id
    doctor = Doctor.objects.get(id=doctor_id)
    patient = request.user.patient
    if request.method == "POST":
        form = forms.AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctorId = doctor  # Gán bác sĩ từ URL
            appointment.patientId = patient   # Gán bệnh nhân từ người dùng đã đăng nhập
            appointment.patientName = patient.get_name  # Lấy tên bệnh nhân
            appointment.doctorName = doctor.get_name  # Lấy tên bác sĩ
            appointment.status = False  # Chưa xác nhận
            appointment.save()  
            return redirect('index_home')  # Sau khi lưu, chuyển đến trang thành công

    else:
        form = forms.AppointmentForm()

    return render(request, 'appointment_form.html', {
        'form': form,
        'doctor': doctor,
        'doctor_id': doctor.id
    })
    
class GetAllPatientDischargeDetail(generics.ListAPIView):
    queryset = PatientDischargeDetails.objects.all() # Lấy tất cả đối tượng Product
    serializer_class = PatientDischargeDetailsSerializer

class GetAllDoctor(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    
class GetAllPatient(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
    
# trả ra json
class GetAppointmentByPatientName(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        name = self.kwargs['name']
        return Appointment.objects.filter(patientId__user__first_name=name)  
    
# trả ra  html
@login_required(login_url='patientlogin')
def get_appointment_by_patient_name(request, name):
    # Lấy danh sách các cuộc hẹn dựa trên tên bệnh nhân
    appointments = Appointment.objects.filter(patientId__user__first_name=name)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments})

@login_required(login_url='patientlogin')
def patient_view_profile(request):
    patient = request.user.patient
    return render(request, 'patient_profile.html', {'patient': patient})