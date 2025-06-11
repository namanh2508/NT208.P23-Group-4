import io,os
import re
from django.contrib.auth import logout
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum
from django.contrib.auth.models import Group,User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date,time
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from hospitalManagement import models
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from hospitalManagement import forms
from django import forms as django_forms
from .forms import UploadTestResultForm
from .forms import AdminSignupForm,DoctorSignupForm,PatientSignupForm,LoginForm,DoctorUserForm,PatientUserForm,CustomUserUpdateForm,AdminDoctorForm,AdminPatientForm,DoctorUserForm,PatientUserForm,AppointmentBookingForm
from django.template.loader import get_template
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView
import random
import easyocr
from PIL import Image
from .models import AI_Metric, Doctor, Patient, Appointment, Service
from google.cloud import vision
#oauth setup
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import secrets
import requests
from django.http import JsonResponse
from xhtml2pdf import pisa
#googlecalendar
from datetime import datetime, timedelta, time
from django.utils.timezone import get_current_timezone, make_aware
from googleapiclient.discovery import build
import math
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
def contactus_view(request):
    return render(request, 'contactus.html')
def index_view(request):
    doctors_list = Doctor.objects.all() 
    
    
    print(f"Số lượng bác sĩ lấy từ DB: {len(doctors_list)}") 

    context = {
        'doctors': doctors_list, 
    }
    
   
    return render(request, 'index_home.html', context)

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

#----------Gửi email otp----------------
def generate_otp():
    return str(random.randint(100000, 999999))
def send_otp_to_email (email):
    otp = generate_otp()

    models.EmailOTP.objects.update_or_create(
        email=email, 
        defaults= {'otp': otp, 'created_at': timezone.now()})
    
    subject = "Mã xác thực OTP của bạn"
    from_email = "noreply@gmail.com"

    html_content = render_to_string("otp_email_template.html", {"otp": otp})
    text_content = strip_tags(html_content)
    try:
        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
    except Exception as e:
        print(f"Lỗi gửi email: {e}")

def send_forgetpass_email(email):
    otp = generate_otp()

    models.EmailOTP.objects.update_or_create(
        email=email, 
        defaults={'otp': otp, 'created_at': timezone.now()}
    )

    subject = "Mã OTP đặt lại mật khẩu của bạn"
    from_email = "noreply@gmail.com"

    html_content = render_to_string("forgetpass_email_template.html", {"otp": otp})
    text_content = strip_tags(html_content)
    try:
        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
    except Exception as e:
        print(f"Lỗi gửi email: {e}")


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

BYPASS_OTP = True  # Toggle this to False in production
def patient_signup_view(request):
    if request.method == "POST":
        # OTP submission
        if 'otp_submit' in request.POST:
            if BYPASS_OTP:
                form_data = request.session.get("pending_form_data")
                if form_data:
                    return complete_signup_from_session(form_data, request)
                messages.error(request, "Không tìm thấy dữ liệu đăng ký.")
                return redirect('patientsignup')

            email = request.session.get("pending_email")
            input_otp = request.POST.get("otp")
            try:
                record = models.EmailOTP.objects.get(email=email)
                if record.otp == input_otp and not record.is_expired():
                    form_data = request.session.get("pending_form_data")
                    return complete_signup_from_session(form_data, request)
                else:
                    messages.error(request, "Mã OTP không đúng hoặc đã hết hạn.")
            except models.EmailOTP.DoesNotExist:
                messages.error(request, "Không tìm thấy yêu cầu xác thực OTP.")
            return render(request, 'verify_otp.html')

        # Form submission
        form = forms.PatientSignupForm(request.POST)
        if form.is_valid():
            form_data = {
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'password': form.cleaned_data['password'],
                'family_phone': form.cleaned_data['family_phone'],
                'weight': form.cleaned_data['weight'],
                'height': form.cleaned_data['height'],
            }

            if BYPASS_OTP:
                return complete_signup_from_session(form_data, request)

            request.session["pending_email"] = form_data['email']
            request.session["pending_form_data"] = form_data
            send_otp_to_email(form_data['email'])
            messages.info(request, "Mã OTP đã được gửi tới email. Vui lòng xác thực.")
            return render(request, 'verify_otp.html')

    else:
        form = forms.PatientSignupForm()
    return render(request, 'patientsignup.html', {'form': form})

def complete_signup_from_session(form_data, request):
    user = models.CustomUser(
        email=form_data['email'],
        username=form_data['username'],
        first_name=form_data['first_name'],
        last_name=form_data['last_name'],
        is_active=True
    )
    user.set_password(form_data['password'])
    user.save()

    patient = models.Patient.objects.create(
        user=user,
        family_phone=form_data['family_phone'],
        weight=form_data['weight'],
        height=form_data['height']
    )
    patient_group, _ = Group.objects.get_or_create(name='PATIENT')
    user.groups.add(patient_group)

    request.session.pop("pending_email", None)
    request.session.pop("pending_form_data", None)
    messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
    return redirect('patientlogin')

# hàm này kích hoạt khi bấm nút login bằng google

def google_login_redirect(request):
    role = request.GET.get('role', 'PATIENT')
    try:
        google_app = SocialApp.objects.get(provider='google')
        client_id = google_app.client_id
    except SocialApp.DoesNotExist:
        return HttpResponse("Google OAuth app not configured", status=500)

    redirect_uri = settings.SITE_URL + "/accounts/google/login/callback/"
    state_token = secrets.token_urlsafe(16)

    request.session['oauth_state'] = state_token
    request.session['oauth_role'] = role
    request.session.modified = True

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        "response_type=code&"
        "scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar&"
        f"state={state_token}&"
        "access_type=offline&"
        "prompt=consent"
    )
    return redirect(google_auth_url)

# xử lý redirect sau khi đăng nhập google thành công

def google_callback(request):
    #chống csrf attack
    stored_state = request.session.get('oauth_state')
    received_state = request.GET.get('state')
    if not stored_state or stored_state != received_state:
        return HttpResponse("Invalid state parameter", status=400)
    request.session.pop('oauth_state', None)
    #lấy role từ google_login_redirect
    role = request.session.get('oauth_role', 'PATIENT')
    #lấy authorization code
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Authorization failed", status=400)

    try:
        app = SocialApp.objects.get(provider='google')
    except SocialApp.DoesNotExist:
        return HttpResponse("Google OAuth app not configured", status=500)

    #dùng authorization code để lấy access token và refresh token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": app.client_id,
        "client_secret": app.secret,
        "redirect_uri": settings.SITE_URL + "/accounts/google/login/callback/",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        return HttpResponse("Failed to get access token", status=400)

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")
    #lấy thông tin cá nhân user
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

    user, created = models.CustomUser.objects.get_or_create(
        username=email, defaults={"email": email, "first_name": name}
    )
    #phân role nếu như là tài khoản mới
    if created:
        if role == 'ADMIN':
            models.Admin.objects.get_or_create(user=user)
            user.is_staff = True
            user.is_superuser = True
        elif role == 'PATIENT':
            models.Patient.objects.get_or_create(user=user)
        elif role == 'DOCTOR':
            models.Doctor.objects.get_or_create(user=user)

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        user.is_active = True
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    #tạo SocialAccount object để lưu access token và refresh token
    account, _ = SocialAccount.objects.get_or_create(
        user=user,
        provider='google',
        uid=user_info['id']
    )
    SocialToken.objects.update_or_create(
        app=app,
        account=account,
        defaults={
            'token': access_token,
            'token_secret': refresh_token or '',
        }
    )
    #chuyển về giao diện chính
    return redirect('afterlogin')

@login_required
def google_link_redirect(request):
    try:
        google_app = SocialApp.objects.get(provider='google')
        client_id = google_app.client_id
    except SocialApp.DoesNotExist:
        return HttpResponse("Google OAuth app not configured", status=500)

    redirect_uri = settings.SITE_URL + "/accounts/google/link/callback/"
    state_token = secrets.token_urlsafe(16)

    request.session['oauth_state'] = state_token
    request.session['link_google'] = True
    request.session.modified = True

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        "response_type=code&"
        "scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar&"
        f"state={state_token}&"
        "access_type=offline&"
        "prompt=consent"
    )
    return redirect(google_auth_url)

@login_required
def google_link_callback(request):
    # Check CSRF-like state
    stored_state = request.session.get('oauth_state')
    received_state = request.GET.get('state')
    if not stored_state or stored_state != received_state:
        return HttpResponse("Invalid state parameter", status=400)
    request.session.pop('oauth_state', None)
    request.session.pop('link_google', None)

    code = request.GET.get("code")
    if not code:
        return HttpResponse("Authorization failed", status=400)

    try:
        app = SocialApp.objects.get(provider='google')
    except SocialApp.DoesNotExist:
        return HttpResponse("Google OAuth app not configured", status=500)

    # Get token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": app.client_id,
        "client_secret": app.secret,
        "redirect_uri": settings.SITE_URL + "/accounts/google/link/callback/",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        return HttpResponse("Failed to get access token", status=400)

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")

    # Get Google profile
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers).json()
    google_uid = user_info['id']

    #Check 1: This Google account already linked to another user
    existing = SocialAccount.objects.filter(provider='google', uid=google_uid)
    if existing:
        return HttpResponse("This Google account is already linked", status=409)

    #Check 2: Current user already linked to another Google account
    already_linked = SocialAccount.objects.filter(provider='google', user=request.user).exclude(uid=google_uid).exists()
    if already_linked:
        return HttpResponse("You have already linked a different Google account.", status=409)

    #Create or update
    account= SocialAccount.objects.create(
        user=request.user,
        provider='google',
        uid=google_uid
    )
    SocialToken.objects.update_or_create(
        app=app,
        account=account,
        defaults={'token': access_token, 'token_secret': refresh_token or ''},
    )

    return redirect('afterlogin')


#lấy Google API credentials cho người dùng, để có thể xài google calendar mà ko phải đăng nhập lại
def get_google_credentials(user):
    try:
        #lấy SocialAccount, access token và refresh token object
        account = SocialAccount.objects.get(user=user, provider='google')
        token = SocialToken.objects.get(account=account, app__provider='google')
        app = SocialApp.objects.get(provider='google')
        #tạo object credentials
        creds = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=app.client_id,
            client_secret=app.secret
        )
        #làm mới access token nếu access token hết hạn mà vẫn còn refresh token, sau đó update database
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token.token = creds.token
            token.save()
        return creds
    #trả về none nếu như thiếu 1 trong 3 object
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist, SocialApp.DoesNotExist):
        return None

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

def request_reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not models.CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email không tồn tại.")
        else:
            send_forgetpass_email(email)
            request.session["reset_email"] = email
            messages.success(request, "OTP đã được gửi đến email.")
            return redirect("verify-otp")
    return render(request, "forget_password_email.html")

def verify_otp_view (request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        email = request.session.get("reset_email")

        try:
            otp_obj = models.EmailOTP.objects.get(email=email, otp=otp)
            if otp_obj.is_expired():
                messages.error(request, "OTP đã hết hạn.")
            else:
                request.session["otp_verified"] = True
                request.session["otp_code"] = otp
                return redirect("reset-password")
        except models.EmailOTP.DoesNotExist:
            messages.error(request, "OTP không hợp lệ.")
    return render(request, "verify_otp.html")

def reset_password_view(request):
    if not request.session.get("otp_verified"):
        messages.error(request, "Bạn chưa xác thực OTP.")
        return redirect("request-reset-password")
    
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        email = request.session.get("reset_email")
        otp = request.session.get("otp_code")

        try:
            otp_obj = models.EmailOTP.objects.get(email=email, otp=otp)
            if otp_obj.is_expired():
                messages.error(request, "OTP đã hết hạn.")
            else:
                user = models.CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                otp_obj.delete()
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                if 'otp_verified' in request.session:
                    del request.session['otp_verified']
                if 'otp_code' in request.session:
                    del request.session['otp_code']
                messages.success(request, "Đặt lại mật khẩu thành công.")
                return redirect("patientlogin")
        except (models.EmailOTP.DoesNotExist, models.CustomUser.DoesNotExist):
            messages.error(request, "Có lỗi xảy ra.")
    return render(request, "reset_password.html")

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        return redirect('doctor-dashboard')
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.filter(user=request.user, user__status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'patient_wait_for_approval.html')
    else: return redirect('index')

#-logout handle
def logout_view(request):
    logout(request)
    return redirect('index')

class ChatPageView(TemplateView):
    template_name = "chatbot.html"

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# trang chủ admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin, login_url='adminlogin')
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount = models.Doctor.objects.filter(user__status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(user__status=False).count()

    patientcount=models.Patient.objects.all().filter(user__status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(user__status=False).count()

    appointmentcount=models.Service.objects.all().filter(status='accepted').count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status='accepted').count()
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
    doctors=models.Doctor.objects.all()
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
def update_doctor_view(request, pk):
    doctor = get_object_or_404(models.Doctor, id=pk)
    user = doctor.user

    if request.method == 'POST':
        form = forms.DoctorUserForm(request.POST, request.FILES, instance=user, doctor=doctor)
        
        print("--- update_doctor_view POST Request Debug ---")
        print("request.POST data:", request.POST)
        print("request.FILES data:", request.FILES)
        
        if form.is_valid():
            print("Form is valid.")
            if 'picture' in form.cleaned_data:
                 print("Cleaned data for picture:", form.cleaned_data.get('picture'))
            try:
                saved_user = form.save() 

                # Nếu bạn muốn cập nhật user.status:
                # saved_user.status = True 
                # saved_user.save()

                print(f"Thông tin bác sĩ cho người dùng '{saved_user.username}' đã được cập nhật.")
                if saved_user.picture:
                    print(f"Đường dẫn ảnh trong DB: {saved_user.picture.name}")
                    print(f"URL ảnh: {saved_user.picture.url}")

                return redirect(reverse('admin-view-doctor'))
            except Exception as e:
                print(f"Lỗi trong quá trình form.save() hoặc xử lý: {e}")
        else:
            print("Form KHÔNG valid.")
            print("Form errors:", form.errors.as_json(escape_html=True))
    else: 
        form = forms.DoctorUserForm(instance=user, doctor=doctor)
        print("--- update_doctor_view GET Request (Form initialized for display) ---")

    context = {
        'form': form,
        'doctor': doctor
    }
    return render(request, 'admin_update_doctor.html', context)

#xem thẻ doctor add
#chức năng thêm doctor
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
   if request.method == 'POST':
       form = forms.DoctorSignupForm(request.POST, request.FILES)
       if form.is_valid():
            user = form.save()
            doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
            user.groups.add(doctor_group)

            return HttpResponseRedirect('admin-view-doctor') 
   else:
            form = forms.DoctorSignupForm()
   return render(request, 'admin_add_doctor.html', {'form': form})

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
    appointments=models.Service.objects.all().filter(status='accepted')
    return render(request,'admin_view_appointment.html',{'appointments':appointments})

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status='accepted')
    return render(request,'admin_approve_appointment.html',{'appointments':appointments})


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    if request.method == 'POST':
        # Create service first
        doctor = models.Doctor.objects.get(id=request.POST.get('doctor'))
        patient = models.Patient.objects.get(id=request.POST.get('patient'))
        
        service = models.Service.objects.create(
            doctor=doctor,
            patient=patient,
            appointmentDate=request.POST.get('appointmentDate'),
            appointmentTime=request.POST.get('appointmentTime'),
            status='pending'
        )
        
        # Then create appointment linked to the service
        appointment = models.Appointment.objects.create(
            service=service,
            method=request.POST.get('method', 'offline'),
            price=request.POST.get('price', 0),
            status=True
        )
        
        return redirect('admin-view-appointment')
    
    # GET request - show form
    doctors = models.Doctor.objects.all()
    patients = models.Patient.objects.all()
    return render(request, 'admin_add_appointment.html', {
        'doctors': doctors,
        'patients': patients
    })







@login_required(login_url='login')
@user_passes_test(is_admin)
def approve_appointment_view(request,id):
    service=models.Service.objects.get(id=id)
    service.status='accepted'
    service.save()
    return redirect(reverse('admin-view-appointment'))



@login_required(login_url='login')
@user_passes_test(is_admin)
def reject_appointment_view(request,id):
    service=models.Service.objects.get(id=id)
    service.status='rejected'
    service.save()
    return redirect('admin-view-appointment')






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
    services = models.Service.objects.filter(doctor=doctor)
    patients = models.Patient.objects.filter(id__in=[service.patient.id for service in services])
    # Tính toán số lượng cuộc hẹn của mỗi bệnh nhân với bác sĩ
    for p in patients:
        p.num_appointments_with_doctor = services.filter(patient=p, status='accepted').count()
    return render(request,'doctor_view_patient.html',{'patients': patients})



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
    appointments=models.Service.objects.all().filter(status="accepted",doctor=doctor).order_by('appointmentDate', 'appointmentTime')
    return render(request,'doctor_view_appointment.html',{'appointments': appointments, 'doctor': doctor})


@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = request.user.doctor  # Lấy thông tin bác sĩ từ người dùng đã đăng nhập
    appointments=models.Appointment.objects.all().filter(status=True,service__doctor=doctor)
    patient_ids = [a.service.patient.id for a in appointments]
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
    appointments=models.Appointment.objects.all().filter(status=True,service__doctor__id=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.service.patient.id)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor, login_url='doctorlogin')
def doctor_dashboard_view(request):
    try:
        doctor = request.user.doctor
    except models.Doctor.DoesNotExist:
        return HttpResponse("Tài khoản này chưa có thông tin bác sĩ!", status=404)

    appointments = models.Service.objects.filter(status='accepted', doctor=doctor).order_by('-id')
    appointmentcount = appointments.count()
    

    mydict = {
        'appointmentcount': appointmentcount,
        'appointments': appointments,
        'doctor': doctor,
        
    }

    return render(request, 'doctor_dashboard.html', context=mydict)
#--------doctor
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor, login_url='doctorlogin')
# def doctor_dashboard_view(request):

#     try:
#         doctor = request.user.doctor
#     except models.Doctor.DoesNotExist:
#         return HttpResponse("Tài khoản này chưa có thông tin bác sĩ!", status=404)
#     appointmentcount = models.Appointment.objects.filter(status=True, doctorId=doctor).count()
#     appointments = models.Appointment.objects.filter(status=True, doctorId=doctor).order_by('-appointmentID')
#     patientdischarged = models.PatientDischargeDetails.objects.filter(assignedDoctorName=request.user.first_name).distinct().count()
#     patient_ids = [a.service.patient.id for a in appointments if a.service and a.service.patient]
#     patients = models.Patient.objects.filter(id__in=patient_ids)
#     patientcount = models.Patient.objects.filter(id__in=patient_ids).count()
#     appointments_and_patients = zip(appointments, patients)
    
#     # Gửi dữ liệu vào template
#     mydict = {
#         'appointmentcount': appointmentcount,  # Tổng số cuộc hẹn chưa hoàn thành
#         'patientdischarged': patientdischarged,  # Số lượng bệnh nhân đã xuất viện
#         'appointments_and_patients': appointments_and_patients,  # Các cuộc hẹn kèm bệnh nhân
#         'doctor': doctor,  # Thông tin bác sĩ (bao gồm ảnh đại diện)
#         'patientcount': patientcount,  # Tổng số bệnh nhân đã khám  
#     }
    
#     return render(request, 'doctor_dashboard.html', context=mydict)
#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient, login_url='patientlogin')
def patient_dashboard_view(request):
        doctors = models.Doctor.objects.all() 
        return render(request, 'patient_dashboard.html', {'doctors': doctors})
#view của UserManagement
# def index_view(request):
#     if request.user.is_authenticated:
#         return redirect('afterlogin')
#     doctors = Doctor.objects.all()
#     return render(request, 'index_home.html', {'doctors': doctors})
def medicine_list_view(request):
    user = request.user
    if is_doctor(user):
        # Doctor: see all medicines in the system
        medicines = models.Medicine.objects.all()
    elif is_patient(user):
        # Patient: see only medicines from their prescriptions
        prescriptions = models.Prescription.objects.filter(service__patient__user=user).select_related('medicine')
        medicines = [p.medicine for p in prescriptions if p.medicine]
    else:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    return render(request, 'medicine_list.html', {'medicines': medicines})
def all_doctors_view(request):
    doctors = models.Doctor.objects.all()  # Lấy tất cả bác sĩ từ database
    return render(request, 'all_doctors.html', {'doctors': doctors})

def add_calendar_reminders(request):
    if request.method == 'POST':
        user = request.user
        creds = get_google_credentials(user)

        if creds is None:
            messages.error(request, "Không tìm thấy quyền Google để thêm lời nhắc.")

        try:
            service = build('calendar', 'v3', credentials=creds)
        except Exception:
            messages.error(request, "Không thể kết nối với Google Calendar.")

        try:
            patient = models.Patient.objects.get(user=user)
            prescriptions = models.Prescription.objects.filter(service__patient=patient)

            if not prescriptions:
                messages.info(request, "Bạn chưa có đơn thuốc nào.")

            total_events = 0
            tz = get_current_timezone() #lấy timezone hiện tại
            today = datetime.now(tz).date() #lấy ngày hôm nay
            TIME_SLOTS = [8, 12, 16, 20]# Khung giờ chia thuốc (24h format)

            for prescription in prescriptions: #mỗi loop là 1 object prescription liên kết khóa ngoại với patient 
                med = prescription.medicine
                if not med or not med.times_per_day or not prescription.amount:
                    continue

                total_pills = prescription.amount #tổng số viên thuốc
                daily_times = med.times_per_day #số lần uống thuốc mỗi ngày
                days_needed = math.ceil(total_pills / daily_times) #số ngày uống thuốc

                for day_offset in range(days_needed): # chạy từ 0->day_needed-1, loop theo từng ngày
                    reminder_count = (
                        daily_times if (day_offset < days_needed - 1) #lấy lần uống thuốc trong ngày để chia theo khung giờ
                        else total_pills % daily_times or daily_times #ngày cuối cùng lấy số dư của tổng số thuốc / số thuốc mỗi ngày hoặc số thuốc mỗi ngày nếu chia hết)
                    )

                    for dose_index in range(reminder_count): # chạy từ 0->reminder_count-1, loop theo từng khung giờ
                        slot_hour = TIME_SLOTS[dose_index % len(TIME_SLOTS)] #xếp từng viên thuốc vào 1 khung giờ, wrap around nếu như dose_index lớn hơn index lớn nhất của time slot
                        event_date = today + timedelta(days=day_offset) #lấy ngày 
                        event_datetime = make_aware(datetime.combine(event_date, time(hour=slot_hour)), tz) #tạo object datetime hoàn chỉnh, kèm theo timezone chính xác
                        #tạo event
                        event = {
                            'summary': f'Dùng thuốc: {med.name}',
                            'description': med.description or '',
                            'start': {
                                'dateTime': event_datetime.isoformat(),
                                'timeZone': 'Asia/Ho_Chi_Minh',
                            },
                            'end': {
                                'dateTime': (event_datetime + timedelta(minutes=30)).isoformat(),
                                'timeZone': 'Asia/Ho_Chi_Minh',
                            },
                        }
                        #add event vào calendar
                        service.events().insert(calendarId='primary', body=event).execute()
                        total_events += 1

            if total_events > 0:
                messages.success(request, f"Đã tạo {total_events} lời nhắc dùng thuốc.")
            else:
                messages.warning(request, "Không có lời nhắc nào được tạo vì thiếu thông tin đơn thuốc.")

        except Exception as e:
            messages.error(request, "Có lỗi xảy ra khi tạo lời nhắc: " + str(e))
    return redirect('patient-dashboard')



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
def get_appointment_by_patient_name(request, user_id):
    patient = get_object_or_404(models.Patient, user_id=user_id)
   
    services = models.Service.objects.filter(patient =patient)
    appointment = models.Appointment.objects.filter(service__in=services)
    return render(request, 'patient_view_appointment.html', {'appointment': appointment} )

# @login_required(login_url='patientlogin')
# def patient_view_profile(request):
#     patient = request.user.patient
#     return render(request, 'patient_profile.html', {'patient': patient})

@login_required(login_url='login')
def patient_profile_view(request):
    patient = Patient.objects.get(user=request.user)
    user = request.user
    context = {
        'patient': patient,
        'user': user,
        'patient_name': f"{user.first_name} {user.last_name}",
        'patient_profile': {
            'dob': user.birthday,
            'gender': user.gender,
            'phone': user.phone,
            'email': user.email,
            'address': patient.address if hasattr(patient, 'address') else None,
            # Thêm các trường thông tin khác nếu có
        }
    }
    return render(request, 'patient_profile.html', context)


@login_required (login_url='patientlogin')
@user_passes_test(is_patient)
def book_appointment(request, id): # id ở đây là user_id của Doctor
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin bệnh nhân của bạn. Vui lòng cập nhật hồ sơ.")
        return redirect('some_profile_update_url_name') # THAY BẰNG URL NAME ĐÚNG

    user_doctor = models.CustomUser.objects.get(id=id)
    selected_doctor_profile = get_object_or_404(Doctor, user=user_doctor)
    
    print(f"Đặt lịch với bác sĩ: {selected_doctor_profile.user.get_full_name()}")

    if request.method == 'POST':
        form = forms.AppointmentBookingForm(request.POST)
        if form.is_valid():
            print("Form hợp lệ (is_valid = True)")
            service = form.save(commit=False)
            service.patient = patient
            # Lấy doctor từ cleaned_data (nếu hidden field gửi đi và form của bạn xử lý đúng)
            # Hoặc an toàn hơn là gán lại từ selected_doctor_profile
            service.doctor = selected_doctor_profile 
            service.status = 'pending'
            service.save()
            
            Appointment.objects.create(
                service=service,
                method=form.cleaned_data['method'],
                status='pending'
            )
            messages.success(request, f"Cuộc hẹn với BS. {service.doctor.user.get_full_name()} vào ngày {service.appointmentDate.strftime('%d-%m-%Y')} lúc {service.appointmentTime.strftime('%H:%M')} đã được yêu cầu.")
            return redirect('patient-view-appointments', user_id=request.user.id)  # Sửa id thành user_id
        else:
            messages.error(request, "Vui lòng sửa các lỗi được chỉ ra trong form.")
            print("Form KHÔNG hợp lệ (is_valid = False)")
            print(f"Lỗi của form: {form.errors.as_json()}")
            # Khi form không hợp lệ, cần render lại với form lỗi và context
            # và đảm bảo trường doctor (nếu có trong form) vẫn là hidden và có giá trị đúng
            if 'doctor' in form.fields:
                 form.fields['doctor'].initial = selected_doctor_profile # Giá trị ban đầu
                 form.fields['doctor'].widget = django_forms.HiddenInput() # Đặt làm trường ẩn
    else: # GET request
        # Khởi tạo form với giá trị ban đầu cho doctor
        form = forms.AppointmentBookingForm(initial={'doctor': selected_doctor_profile})
        # Chuyển widget của trường doctor thành HiddenInput
        if 'doctor' in form.fields:
            form.fields['doctor'].widget = django_forms.HiddenInput()

    page_title = f"Đặt lịch khám với bác sĩ {selected_doctor_profile.user.get_full_name()}"
    service = models.Service.objects.filter(doctor=selected_doctor_profile) 
    context = {
        'selected_doctor_profile': selected_doctor_profile, 
        'form': form,
        'page_title': page_title,
        'service': service
    }
    return render(request, 'patient_book_appointment.html', context)

def check_service_by_date(request, date):
    services = Service.objects.filter(appointmentDate=date)
    data = [{'id': s.id, 'name': s.name} for s in services]
    return JsonResponse({'services': data})


def GetPatient(request,user_id):
    patient = models.Patient.objects.get(user_id=user_id)
    if not patient:
        return HttpResponse("Patient not found", status=404)
    return render(request, 'patient_profile.html', {'patient': patient})
    googlelinked = request.user.socialaccount_set.filter(provider='google').exists()
    return render(request, 'patient_profile.html', {
        'patient': patient,
        'googlelinked': googlelinked
    })
def Get_Doctor_Detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

@login_required(login_url='patientlogin')
def cancel_appointment_view(request, appointment_id):
    try:
        appointment = models.Appointment.objects.get(id=appointment_id)
        
        # Kiểm tra xem người dùng hiện tại có phải là chủ của cuộc hẹn
        if appointment.service.patient.user != request.user:
            messages.error(request, "Bạn không có quyền hủy cuộc hẹn này.")
            return redirect('patient-view-appointments', user_id=request.user.id)
            
        # Xóa cuộc hẹn
        appointment.delete()
        
        messages.success(request, "Cuộc hẹn đã được hủy thành công.")
        return redirect('patient-view-appointments', user_id=request.user.id)
        
    except models.Appointment.DoesNotExist:
        messages.error(request, "Không tìm thấy cuộc hẹn.")
        return redirect('patient-view-appointments', user_id=request.user.id)
    
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def extract_text_from_image(image_path):
    # Placeholder implementation
    logger.warning("extract_text_from_image function is not implemented.")
    return ""

def analyze_test_result(text):
    # Placeholder implementation
    logger.warning("analyze_test_result function is not implemented.")
    return []

def call_dermatology_ai_api(image_path):
    # Placeholder implementation
    logger.warning("call_dermatology_ai_api function is not implemented.")
    return {"diagnosis": None, "confidence": None}

# @csrf_exempt
# def upload_image_view(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 ai_record = form.save(commit=False)
                
#                 # Tự động xác định loại ảnh
#                 auto_type, confidence = detect_record_type_by_cnn(request.FILES['image'])
#                 ai_record.record_type = auto_type
#                 ai_record.save()

#                 if ai_record.record_type == 'lab_report':
#                     text = extract_text_from_image(ai_record.image.path)
#                     metrics = analyze_test_result(text)
#                     for m in metrics:
#                         AI_Metric.objects.create(
#                             ai_record=ai_record,
#                             name=m['name'],
#                             value=m['value'],
#                             unit=m['unit'],
#                             status=m['status'],
#                             reference_range=m['range']
#                         )
#                 else:  # dermatology or xray
#                     result = call_dermatology_ai_api(ai_record.image.path)
#                     ai_record.diagnosis = result.get('diagnosis')
#                     ai_record.confidence = result.get('confidence')
#                     ai_record.save()

#                 return redirect('ai_upload_success')
#             except Exception as e:
#                 logger.error(f"Error processing uploaded image: {e}")
#                 messages.error(request, "There was an error processing the image. Please try again.")
#         else:
#             messages.error(request, "Invalid form submission. Please check the input.")
#     else:
#         form = UploadForm()
#     return render(request, 'ai_upload.html', {'form': form})


# def predict_view(request):
#     if request.method == 'POST' and 'image' in request.FILES:
#         image_file = request.FILES['image']
#         result = detect_record_type_by_cnn(image_file)
#         return JsonResponse({'result': result})
#     return JsonResponse({'error': 'No image uploaded'}, status=400)

def parse_blood_test_results(ocr_text):
    """
    Phân tích văn bản OCR thô từ kết quả xét nghiệm huyết học
    để trích xuất các cặp (chỉ số, giá trị).
    """
    # Danh sách các từ khóa xét nghiệm chúng ta quan tâm
    TEST_KEYWORDS = [
        'WBC', 'NEU', 'LYM', 'MONO', 'BASO', 'EOS',
        'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC',
        'RDW', 'PLT', 'MPV'
    ]
    
    results = {}
    lines = ocr_text.split('\n')

    for i, line in enumerate(lines):
        for keyword in TEST_KEYWORDS:
            # Tìm xem dòng có chứa từ khóa không
            if keyword in line:
                # Tìm giá trị số. Chúng ta sẽ tìm ở dòng hiện tại và 2 dòng tiếp theo
                # phòng trường hợp OCR tách số ra dòng khác.
                value_found = None
                search_area = lines[i:i+3] # Vùng tìm kiếm giá trị
                
                for search_line in search_area:
                    # Regex để tìm số thập phân hoặc số nguyên
                    match = re.search(r'\b\d+\.?\d*\b', search_line)
                    if match:
                        # Đảm bảo số tìm được không phải là một phần của từ khóa khác
                        # và chưa được gán cho một kết quả nào
                        potential_value = match.group(0)
                        if potential_value not in results.values():
                           value_found = potential_value
                           break # Thoát khỏi vòng lặp tìm kiếm khi đã thấy giá trị
                
                if value_found:
                    results[keyword] = value_found
    
    return results
try:
    reader = easyocr.Reader(['vi', 'en'], gpu=False)
    print("EasyOCR reader initialized successfully.")
except Exception as e:
    reader = None
    print(f"Error initializing EasyOCR reader: {e}")

@login_required(login_url='patientlogin')
def upload_test_result(request):
    if reader is None:
        messages.error(request, "Lỗi: Dịch vụ OCR chưa sẵn sàng. Vui lòng liên hệ quản trị viên.")
        return redirect('patient-dashboard')

    if request.method == 'POST':
        form = UploadTestResultForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.patient = request.user.patient

            if instance.test_type == 'other':
                instance.test_type = form.cleaned_data.get('custom_test_name', 'Khác')

            # Lưu instance mà không có file trước để lấy ID (nếu cần)
            # Hoặc chỉ lưu các trường khác file
            instance.save()

            # Kiểm tra xem có file nào được upload không
            if 'file' in request.FILES:
                try:
                    uploaded_file = request.FILES['file']
                    
                    
                    
                    # 1. Tua lại con trỏ về đầu file
                    uploaded_file.seek(0)
                    
                    # 2. Đọc nội dung file
                    file_bytes = uploaded_file.read()

                    # 3. (Phòng vệ) Kiểm tra xem buffer có thực sự rỗng không
                    if not file_bytes:
                        raise ValueError("File được tải lên không có nội dung hoặc không thể đọc được.")
                        
                    

                    

                   
                    
                    detailed_result = reader.readtext(file_bytes)
                    
                    
                    text_list = [item[1] for item in detailed_result]

                    
                    ocr_text = "\n".join(text_list)
                    
                    parsed_results = parse_blood_test_results(ocr_text)
                    
                    
                    formatted_text = "Kết quả phân tích tự động:\n"
                    formatted_text += "----------------------------\n"
                    for key, value in parsed_results.items():
                        formatted_text += f"{key:<10}: {value}\n" # Định dạng cột
                    
                    
                    instance.ocr_text = formatted_text # Lưu dạng đã định dạng
                    
                    instance.save(update_fields=['ocr_text'])

                    messages.success(request, "Kết quả xét nghiệm đã được tải lên và xử lý bằng EasyOCR thành công!")
                    return redirect('patient_view_test_result', id=instance.id)

                except Exception as e:
                    messages.error(request, f"Lỗi khi xử lý ảnh với EasyOCR: {e}")
                    # Vẫn chuyển hướng để người dùng không bị kẹt
                    return redirect('patient_view_test_result', id=instance.id)
            else:
                messages.warning(request, "Thông tin đã được lưu nhưng bạn chưa tải lên file kết quả.")
                return redirect('patient-dashboard')
        else:
            messages.error(request, "Có lỗi trong form. Vui lòng kiểm tra lại.")
    else:
        form = UploadTestResultForm()

    return render(request, 'upload_test_result.html', {'form': form})


@login_required(login_url='patientlogin')
def view_test_result(request, id):
    try:
        test_result = request.user.patient.upload_test_results.get(id=id)
    except Exception as e:
        messages.error(request, "Không tìm thấy kết quả xét nghiệm.")
        return redirect('patient-dashboard')

    # Chúng ta không cần truyền extracted_text nữa vì nó đã được lưu trong test_result.ocr_text
    return render(request, 'test_result.html', {
        'test_result': test_result,
        'extracted_text': test_result.ocr_text # Lấy text trực tiếp từ model
    })


