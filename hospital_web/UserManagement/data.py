from UserManagement.models import Users,Appointments
patient = Users.objects.get(email="namanh@gmail.com")
doctor = Users.objects.get(email="vankhoi@gmail.com")



user1 = Users.objects.create(
    userName="Phùng Văn Nam Anh",
    email="namanh@gmail.com",
    password="namanh",  # Cần mã hóa password trong thực tế
    date_of_birth="2005-01-02",
    phone_number="0987654321",
    biological_sex=0,  # Male
    role=1,  # Doctor
    specialty="Cardiology"
)

user2 = Users.objects.create(
    userName="Lê Văn Khôi",
    email="vankhoi@gmail.com",
    password="vankhoi",
    date_of_birth="2005-01-01",
    phone_number="0123456789",
    biological_sex=1,  # Female
    role=0  # Patient
)

appointment = Appointments.objects.create(
    patientID=patient,
    doctorID=doctor,
    appointment_date="2025-03-25",
    status="scheduled",
    reason="Đau đầu kéo dài"
)

