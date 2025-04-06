from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.db.models import Sum
from django.contrib.auth.models import Group,User
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from hospitalManagement import models
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from hospitalManagement import forms
from .forms import CustomUserSignupFormm,AdminSignupForm,DoctorSignupForm,PatientSignupForm,LoginForm,DoctorUserForm,PatientUserForm,CustomUserUpdateForm,AdminDoctorForm,AdminPatientForm,DoctorUserForm,PatientUserForm,AppointmentBookingForm
from django.template.loader import get_template
#oauth setup
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialApp
import secrets
import requests
from .models import CustomUser,Admin,Doctor,Patient,Appointment
# Create your views here.

#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def home_view(request):
    return render(request,'index.html')
def aboutus_view(request):
    return render(request, 'aboutus.html')
def index_view(request):
    return render(request, 'index_home.html')

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated and request.user.is_admin():
        return redirect('admin-dashboard')
    return render(request,'adminlogin.html')

#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated and request.user.is_doctor():
        return redirect('doctor-dashboard')
    return render(request,'doctorlogin.html')


#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated and request.user.is_patient():
        return redirect('patient-dashboard')
    return render(request,'patient.html')

#----------Signup Views----------------

def admin_signup_view(request):
    if request.method == "POST":
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            admin_group, _ = Group.objects.get_or_create(name='ADMIN')
            user.groups.add(admin_group)
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('adminlogin')
    else:
        form = forms.AdminSignupForm()
        print(form.errors)
    return render(request, 'adminsignup.html', {'form': form})


def doctor_signup_view(request):
    if request.method == "POST":
        form = forms.DoctorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
            user.groups.add(doctor_group)
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('doctorlogin')
    else:
        form = forms.DoctorSignupForm()
    return render(request, 'doctorsignup.html', {'form': form})

def patient_signup_view(request):
    if request.method == "POST":
        form = forms.PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            patient_group, _ = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(patient_group)
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('patientlogin')
    else:
        form = forms.DoctorSignupForm()
    return render(request, 'patientsignup.html', {'form': form})


#google login
def google_login_redirect(request):
    role = request.GET.get('role', 'PATIENT')
    try:
        google_app = SocialApp.objects.get(provider='google')
        client_id = google_app.client_id
    except SocialApp.DoesNotExist:
        client_id = '956299204451-suo8i077gtc4n3tolq3ba1ggqa3ovgue.apps.googleusercontent.com'
    redirect_uri = settings.SITE_URL + "/accounts/google/login/callback/"
    # Generate a secure random state token
    state_token = secrets.token_urlsafe(16)
    # Store state in the session for verification later
    request.session['oauth_state'] = state_token
    request.session['oauth_role'] = role  # Store role in session
    request.session.modified = True  # Ensure session updates
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        "scope=email%20profile&"
        "response_type=code&"
        f"state={state_token}&"
        "access_type=online"
    ) 
    return redirect(google_auth_url)

def google_callback(request):
    stored_state = request.session.get('oauth_state')
    received_state = request.GET.get('state')

    if not stored_state or stored_state != received_state:
        return HttpResponse("Invalid state parameter", status=400)

    request.session.pop('oauth_state', None)
    
    role = request.session.get('oauth_role', 'PATIENT')  # Retrieve role from session

    code = request.GET.get("code")
    if not code:
        return HttpResponse("Authorization failed", status=400)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.SITE_URL + "/accounts/google/login/callback/",
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        return HttpResponse("Failed to get access token", status=400)

    access_token = token_data["access_token"]

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    if user_info_response.status_code != 200:
        return HttpResponse("Failed to retrieve user information", status=400)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return HttpResponse("Failed to retrieve user email", status=400)

    # Get or create the user
    user, _ = models.CustomUser.objects.get_or_create(
    username=name, defaults={"email": email, "first_name": name}
    )
    if role == 'ADMIN':
        admin, _ = models.Admin.objects.get_or_create(user=user)
        user.is_staff = True  # Allow access to admin site
        user.is_superuser = True  # Optionally make them a superuser for full access
        user.save()
    if role == 'PATIENT':
        patient, _ = models.Patient.objects.get_or_create(user=user)
    if role == 'DOCTOR':
        doctor, _ = models.Doctor.objects.get_or_create(user=user)
    # Add user to the group
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)
    # Log the user in
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect("afterlogin")


#login view
def admin_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Django's built-in login form
        if form.is_valid():
            user = form.get_user()
            if is_admin(user):
                login(request, user)
                return redirect("admin-dashboard")
            else:
                form.add_error(None, "Access Denied: You are not an Admin.")
        else:
            form.add_error(None, "Thông tin đăng nhập không chính xác.")

    else:
        form = AuthenticationForm()
    return render(request, "adminlogin.html", {"form": form})
def doctor_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_doctor(user):
                login(request, user)
                return redirect("doctor-dashboard")
            else:
                form.add_error(None, "Access Denied: You are not a Doctor.")

    else:
        form = AuthenticationForm()

    return render(request, "doctorlogin.html", {"form": form})

def patient_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_patient(user):
                login(request, user)
                return redirect("patient-dashboard")
            else:
                form.add_error(None, "Access Denied: You are not a patient.")

    else:
        form = AuthenticationForm()

    return render(request, "patientlogin.html", {"form": form})

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        return redirect('doctor-dashboard')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'patient_wait_for_approval.html')
    else: return redirect('index')

#-logout handle
def logout_view(request):
    logout(request)
    return redirect('index')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# trang chủ admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admin_dashboard.html',context=mydict)

#-------click vào mục doctor----------------------------------------------------
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'admin_doctor.html')

#xem thẻ doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})

#chức năng xóa doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')

#chức năng chỉnh sửa doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'admin_update_doctor.html',context=mydict)

#xem thẻ doctor add
#chức năng thêm doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'admin_add_doctor.html',context=mydict)

#xem thẻ doctor approve
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'admin_approve_doctor.html',{'doctors':doctors})

#chức năng approve doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))
#chức năng reject doctor

@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')

#xem thẻ specialist doctor
#xem thong tin các khoa của doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor_specialisation.html',{'doctors':doctors})

# Hàm hiển thị trang quản lý bệnh nhân cho admin
@login_required(login_url='login')  # Chỉ cho phép người đã đăng nhập
@user_passes_test(is_admin)  # Kiểm tra xem người dùng có phải admin không
def admin_patient_view(request):
    return render(request, 'admin_patient.html')


# Hàm hiển thị danh sách bệnh nhân đã được duyệt
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_view_patient.html', {'patients': patients})


# Hàm xóa bệnh nhân khỏi hệ thống
@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')


# Hàm cập nhật thông tin bệnh nhân
@login_required(login_url='login')
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}

    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')

    return render(request, 'admin_update_patient.html', context=mydict)


# Hàm thêm bệnh nhân mới vào hệ thống
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}

    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')

    return render(request, 'admin_add_patient.html', context=mydict)


# Hàm hiển thị danh sách bệnh nhân cần phê duyệt
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'admin_approve_patient.html', {'patients': patients})


# Hàm phê duyệt bệnh nhân
@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin-approve-patient'))


# Hàm từ chối bệnh nhân và xóa họ khỏi hệ thống
@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


# Hàm hiển thị danh sách bệnh nhân chuẩn bị xuất viện
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_discharge_patient.html', {'patients': patients})


# Hàm xử lý xuất viện bệnh nhân và tạo hóa đơn
@login_required(login_url='login')
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = (date.today() - patient.admitDate)
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days

    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }

    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']) * int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) +
                     int(request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)

        # Lưu thông tin xuất viện vào cơ sở dữ liệu
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST['medicineCost'])
        pDD.roomCharge = int(request.POST['roomCharge']) * int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + \
                    int(request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        pDD.save()
        return render(request, 'patient_final_bill.html', context=patientDict)

    return render(request, 'patient_generate_bill.html', context=patientDict)


# Hàm chuyển trang HTML thành file PDF
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


# Hàm tạo file PDF hóa đơn xuất viện
def download_pdf_view(request, pk):
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'symptoms': dischargeDetails[0].symptoms,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html', dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'admin_appointment.html')



@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'admin_add_appointment.html',context=mydict)



@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(appointmentID=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(appointmentID=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

#--------doctor
@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):

    doctor = request.user.doctor 
    appointmentcount = models.Appointment.objects.filter(status=True, doctorId=doctor).count()
    appointments = models.Appointment.objects.filter(status=True, doctorId=doctor).order_by('-appointmentID')
    patientdischarged = models.PatientDischargeDetails.objects.filter(assignedDoctorName=request.user.first_name).distinct().count()
    patient_ids = [a.patientId.id for a in appointments]
    patients = models.Patient.objects.filter(id__in=patient_ids)
    patientcount = models.Patient.objects.filter(id__in=patient_ids).count()
    appointments_and_patients = zip(appointments, patients)
    
    # Gửi dữ liệu vào template
    mydict = {
        'appointmentcount': appointmentcount,  # Tổng số cuộc hẹn chưa hoàn thành
        'patientdischarged': patientdischarged,  # Số lượng bệnh nhân đã xuất viện
        'appointments_and_patients': appointments_and_patients,  # Các cuộc hẹn kèm bệnh nhân
        'doctor': doctor,  # Thông tin bác sĩ (bao gồm ảnh đại diện)
        'patientcount': patientcount,  # Tổng số bệnh nhân đã khám  
    }
    
    return render(request, 'doctor_dashboard.html', context=mydict)




@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor_patient.html',context=mydict)



@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    doctor = request.user.doctor  # Lấy thông tin bác sĩ từ người dùng đã đăng nhập
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=doctor)
    patient_ids = [a.patientId.id for a in appointments]
    patients = models.Patient.objects.filter(id__in=patient_ids)
    # Tính toán số lượng cuộc hẹn của mỗi bệnh nhân với bác sĩ
    for p in patients:
        p.num_appointments_with_doctor = appointments.filter(patientId=p).count()
    appointments = zip(appointments, patients)
    return render(request,'doctor_view_patient.html',{'appointments': appointments, 'patients': patients})



@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = request.user.doctor  # Lấy thông tin bác sĩ từ người dùng đã đăng nhập
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=doctor)
    patient_ids = [a.patientId.id for a in appointments]
    patients = models.Patient.objects.filter(id__in=patient_ids)
    appointments = zip(appointments, patients)
    return render(request,'doctor_view_appointment.html',{'appointments': appointments, 'doctor': doctor})


@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = request.user.doctor  # Lấy thông tin bác sĩ từ người dùng đã đăng nhập
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=doctor)
    patient_ids = [a.patientId.id for a in appointments]
    patients = models.Patient.objects.filter(id__in=patient_ids)
    print("Appointments:")
    for a in appointments:
        print(f"Appointment ID: {a.appointmentID}, Doctor: {a.doctorName}, Patient: {a.patientName}, Date: {a.appointmentDate}")
    print("Patients:")
    for p in patients:
        print(f"Patient ID: {p.id}, Name: {p.user.first_name} {p.user.last_name}, Mobile: {p.mobile}")
    appointments = zip(appointments, patients)
    return render(request,'doctor_delete_appointment.html',{'appointments': appointments, 'doctor': doctor})



@login_required(login_url='login')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def doctor_dashboard_view(request):
    return None

#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def patient_dashboard_view(request):
    return None
#view của UserManagement
# def index_view(request):
#     if request.user.is_authenticated:
#         return redirect('afterlogin')
#     doctors = Doctor.objects.all()
#     return render(request, 'index_home.html', {'doctors': doctors})

# def all_doctors_view(request):
#     doctors = Doctor.objects.all()  # Lấy tất cả bác sĩ từ database
#     return render(request, 'all_doctors.html', {'doctors': doctors})

# def patient_signup_view(request):
#     userForm=forms.PatientUserForm()
#     patientForm=forms.PatientForm()
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST)
#         patientForm=forms.PatientForm(request.POST,request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             patient=patientForm.save(commit=False)
#             patient.user=user
#             patient=patient.save()
#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)
#         return redirect('patientlogin')
#     return render(request,'patientsignup.html',context=mydict)

# def patientlogin_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)  # Django�s built-in login form
#         if form.is_valid():
#             user = form.get_user()
#             if user.groups.filter(name="PATIENT").exists():
#                 login(request, user)
#                 return redirect("patient-dashboard")
#             else:
#                 form.add_error(None, "Không tìm thấy tài khoản của bạn")

#     else:
#         form = AuthenticationForm()

#     return render(request, "patientlogin.html", {"form": form})

# def logout_view(request):
#     logout(request)
#     return redirect('index_home')

# def is_patient(user):
#     return user.groups.filter(name='PATIENT').exists()

# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_dashboard_view(request):
#     if request.user.is_authenticated:
#         doctors = Doctor.objects.all() 
#         return render(request, 'patient_dashboard.html', {'doctors': doctors})
#     else:
#         return redirect('patientlogin')

# @login_required(login_url='/IV-Medical/patientsignup')
# def appointment_view(request, doctor_id):
#     # Lấy thông tin bác sĩ từ doctor_id
#     doctor = Doctor.objects.get(id=doctor_id)
#     patient = request.user.patient
#     if request.method == "POST":
#         form = forms.AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.doctorId = doctor  # Gán bác sĩ từ URL
#             appointment.patientId = patient   # Gán bệnh nhân từ người dùng đã đăng nhập
#             appointment.patientName = patient.get_name  # Lấy tên bệnh nhân
#             appointment.doctorName = doctor.get_name  # Lấy tên bác sĩ
#             appointment.status = False  # Chưa xác nhận
#             appointment.save()
#             return redirect('index_home')  # Sau khi lưu, chuyển đến trang thành công

#     else:
#         form = forms.AppointmentForm()

#     return render(request, 'appointment_form.html', {
#         'form': form,
#         'doctor': doctor,
#         'doctor_id': doctor.id
#     })
    
# class GetAllPatientDischargeDetail(generics.ListAPIView):
#     queryset = PatientDischargeDetails.objects.all() # Lấy tất cả đối tượng Product
#     serializer_class = PatientDischargeDetailsSerializer

# class GetAllDoctor(generics.ListAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = [AllowAny]
    
# class GetAllPatient(generics.ListAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [AllowAny]
    
    
# # trả ra json
# class GetAppointmentByPatientName(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         name = self.kwargs['name']
#         return Appointment.objects.filter(patientId__user__first_name=name)  
    
# # trả ra  html
@login_required(login_url='patientlogin')
def get_appointment_by_patient_name(request, name):
    # Lấy danh sách các cuộc hẹn dựa trên tên bệnh nhân
    appointments = models.Appointment.objects.filter(patientId__user__first_name=name)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments})

# @login_required(login_url='patientlogin')
# def patient_view_profile(request):
#     patient = request.user.patient
#     return render(request, 'patient_profile.html', {'patient': patient})


@login_required (login_url='patientlogin')
@user_passes_test(is_patient)
def book_appointment(request):
    try:
        # Get the patient profile associated with the logged-in user
        # Assumes a OneToOne relationship exists and profile is created
        patient = request.user.patient
    except Patient.DoesNotExist:
        # Handle cases where the user doesn't have a Patient profile
        messages.error(request, "You need a patient profile to book appointments.")
        # Redirect to a profile creation page or dashboard
        return redirect('patient-dashboard')

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            # Create Service instance but don't save to DB yet
            service = form.save(commit=False)
            # Assign the logged-in patient
            service.patient = patient
            # Set initial status (as defined in model default, but explicit is fine)
            service.status = 'pending'
            # Now save the Service instance to the database
            service.save()

            messages.success(request, f"Appointment requested successfully for {service.appointmentDate.strftime('%Y-%m-%d')} at {service.appointmentTime.strftime('%H:%M')} with {service.doctor}. You will be notified upon confirmation.")
            # Redirect to a success page or the patient's appointment list
            return redirect('patient-view-appointment') # CHANGE THIS to your success/list URL name

        else:
            # Form is invalid, errors will be displayed in the template
            messages.error(request, "Please correct the errors below.")
    else:
        # GET request, display a blank form
        form = AppointmentBookingForm()

    context = {
        'form': form,
        'page_title': 'Book an Appointment' # Optional: for template title
    }
    return render(request, 'patient_book_appointment.html', context) # CHANGE THIS template path