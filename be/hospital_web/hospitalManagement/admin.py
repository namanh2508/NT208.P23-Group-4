from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Doctor, Patient, Admin as HospitalAdmin,
    Service, Record, AI_Record, Appointment, Test,
    Medicine, Prescription, Bill, TestParameter, AI_Metric
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
    list_display = ('id', 'patient', 'doctor', 'appointmentDate', 'appointmentTime', 'status','type')
    list_filter = ('status','type',)
    search_fields = ('patient__user__username', 'doctor__user__username','type')

# ---------- Record Admin ----------
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'record_date')
    list_filter = ('record_date',)
    search_fields = ('patient__user__username', 'doctor__user__username')

# ---------- AI Record Admin ----------
@admin.register(AI_Record)
class AIRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'created_at', 'record_type')
    list_filter = ('created_at',)
    search_fields = ('patient__user__username',)
# ---------- AI Metric Admin ----------
@admin.register(AI_Metric)
class AIMetricAdmin(admin.ModelAdmin):
    list_display = ('id',  'name', 'value','status')
    list_filter = ('name','status')
    search_fields = ('patient__user__username', 'name')
# ---------- Appointment Admin ----------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'method', 'price', 'status')
    list_filter = ('status', 'method')
    search_fields = ('service__patient__user__username',)

# ---------- Test Admin ----------
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', )
    search_fields = ('service__patient__user__username',)
    
# ---------- Test Parameter Admin ----------
@admin.register(TestParameter)
class TestParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'status', 'unit')
    list_filter = ('name',)
    search_fields = ('test__service__patient__user__username', 'name')

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

