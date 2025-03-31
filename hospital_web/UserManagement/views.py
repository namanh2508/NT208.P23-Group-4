from django.shortcuts import redirect, render
from hospitalManagement import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse
# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'index_home.html')

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


