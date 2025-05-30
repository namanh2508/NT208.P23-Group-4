

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render # Thêm render nếu bạn có doctor_video_room_view
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.contrib.auth.decorators import login_required,user_passes_test
# Import các model từ app hospitalManagement (hoặc app chứa model của bạn)
from hospitalManagement.models import Appointment, Service, Patient, Doctor, CustomUser 
# Import từ thư viện OpenTok (Vonage)

from hospitalManagement import models


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def lam_tron_gio_ve_30_phut(thoi_gian_obj):
    # Bây giờ 'datetime' là lớp datetime.datetime, và 'time' là lớp datetime.time
    if not isinstance(thoi_gian_obj, (datetime, time)): # << ĐÃ SỬA
        raise TypeError("Đầu vào phải là đối tượng datetime.datetime hoặc datetime.time")

    phut_hien_tai = thoi_gian_obj.minute
    
    phut_moi = 0
    if phut_hien_tai >= 30:
        phut_moi = 30
    
    return thoi_gian_obj.replace(minute=phut_moi, second=0, microsecond=0)


def doctor_video_room_view(request, doctor_user_id):
    user = request.user
    if is_patient(user):
        patient_profile_for_check = Patient.objects.get(user=user)
        target_doctor_user_for_check = models.CustomUser.objects.get(id=doctor_user_id)
        target_doctor_profile_for_check = get_object_or_404(Doctor, user=target_doctor_user_for_check)
        current_date = timezone.now().date()
        utc_now = timezone.now()
        current_time = timezone.localtime(utc_now)
        service_now = Service.objects.filter(
            patient=patient_profile_for_check,
            doctor=target_doctor_profile_for_check,
            appointmentDate=current_date,
            appointmentTime=lam_tron_gio_ve_30_phut(current_time).time()
        )
        if (service_now):
            return render(request, 'meeting.html', {'user': user, 'room_id': doctor_user_id, 'role': 'patient'})
        else:
            print("khong co")
            return HttpResponseForbidden("Bạn chưa đến giờ hẹn hoặc không có quyền vào phòng này.")
    
    print("username: ",user.username)
    if is_doctor(user):
        return render(request, 'meeting.html', {'user': user, 'room_id': doctor_user_id, 'role': 'doctor'})
    else:
        return HttpResponseForbidden("Bạn không có quyền truy cập vào phòng họp này.")


