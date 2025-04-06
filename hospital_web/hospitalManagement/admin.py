# from django.contrib import admin
# from .models import Doctor,Patient,Appointment,PatientDischargeDetails
# # Register your models here.
# class DoctorAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Doctor, DoctorAdmin)

# class PatientAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Patient, PatientAdmin)

# class AppointmentAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Appointment, AppointmentAdmin)

# class PatientDischargeDetailsAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Doctor, Patient, Admin as HospitalAdmin,
    Service, Record, AI_Record, Appointment, Test,
    Medicine, Prescription, Bill
)

# ---------- CustomUser Admin ----------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'birthday', 'status', 'is_staff')
    list_filter = ('gender', 'status', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("picture", "phone", "gender", "birthday", "multi_factor_enabled", "ip_address_last_login", "status")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("picture", "phone", "gender", "birthday", "multi_factor_enabled", "ip_address_last_login", "status")
        }),
    )

# ---------- Doctor Admin ----------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'get_department')
    list_filter = ('department',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# ---------- Patient Admin ----------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'family_phone', 'weight', 'height')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# ---------- Admin Admin ----------
@admin.register(HospitalAdmin)
class HospitalAdminAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# ---------- Service Admin ----------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointmentDate', 'appointmentTime', 'status')
    list_filter = ('status',)
    search_fields = ('patient__user__username', 'doctor__user__username')

# ---------- Record Admin ----------
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'record_date')
    list_filter = ('record_date',)
    search_fields = ('patient__user__username', 'doctor__user__username')

# ---------- AI Record Admin ----------
@admin.register(AI_Record)
class AIRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'record_date', 'glucose', 'blood_pressure')
    list_filter = ('record_date',)
    search_fields = ('patient__user__username',)

# ---------- Appointment Admin ----------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'method', 'price', 'status')
    list_filter = ('status', 'method')
    search_fields = ('service__patient__user__username',)

# ---------- Test Admin ----------
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'glucose', 'blood_pressure', 'blood_group')
    search_fields = ('service__patient__user__username',)

# ---------- Medicine Admin ----------
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'times_per_day')
    search_fields = ('name', 'brand')

# ---------- Prescription Admin ----------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'service', 'amount', 'total_price')
    search_fields = ('service__patient__user__username', 'medicine__name')

# ---------- Bill Admin ----------
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'release_date', 'pay_date', 'total_price', 'status', 'method')
    list_filter = ('status', 'method')
    search_fields = ('patient__user__username',)

