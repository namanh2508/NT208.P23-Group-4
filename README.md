# IV-Medical - Hệ thống Quản lý Bệnh viện

## Giới thiệu

IV-Medical là một hệ thống quản lý bệnh viện toàn diện được xây dựng bằng Django và React. Hệ thống cung cấp các tính năng quản lý bệnh nhân, bác sĩ, lịch hẹn khám bệnh, và tích hợp AI để hỗ trợ chẩn đoán y tế.

## ✨ Tính năng chính

### 🏥 Quản lý Người dùng
- **Đăng ký/Đăng nhập** cho 3 vai trò: Admin, Bác sĩ, Bệnh nhân
- **Đăng nhập Google OAuth** tích hợp
- **Xác thực OTP** qua email
- **Quản lý profile** cá nhân với ảnh đại diện

### 👨‍⚕️ Dành cho Bác sĩ
- Dashboard theo dõi lịch khám
- Quản lý thông tin bệnh nhân
- Xem lịch hẹn và thống kê
- Tạo đơn thuốc và hồ sơ bệnh án

### 🏥 Dành cho Admin
- Quản lý tài khoản bác sĩ và bệnh nhân
- Duyệt/từ chối đăng ký mới
- Thống kê tổng quan hệ thống
- Quản lý lịch hẹn toàn bộ bệnh viện

### 👤 Dành cho Bệnh nhân
- Đặt lịch khám với bác sĩ
- Xem lịch sử khám bệnh
- Upload kết quả xét nghiệm với **OCR tự động**
- **AI phân tích** kết quả xét nghiệm
- Tích hợp **Google Calendar** để nhắc nhở uống thuốc
- **Video call** tư vấn trực tuyến

### 🤖 Tính năng AI
- **OCR**: Đọc tự động kết quả xét nghiệm từ ảnh
- **Gemini AI**: Phân tích và tư vấn kết quả xét nghiệm
- **Chatbot**: Hỗ trợ tư vấn sức khỏe 24/7

### 💳 Thanh toán
- Tích hợp **PayOS** thanh toán online
- Webhook xử lý trạng thái thanh toán tự động

## 🛠️ Công nghệ sử dụng

### Backend
- **Django 5.1** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database chính
- **JWT** - Authentication
- **Google OAuth2** - Social login
- **EasyOCR** - Optical Character Recognition
- **Google Gemini AI** - Text analysis
- **PayOS** - Payment gateway

### Frontend
- **HTML/CSS/JavaScript** - Core frontend
- **Bootstrap** - UI framework
- **Widget Tweaks** - Form styling

### AI & Machine Learning
- **Google Gemini 2.0** - Text analysis và chatbot
- **EasyOCR** - Đọc text từ ảnh
- **Ollama** - Local AI model (Phi3)

### Cloud Services
- **Google Calendar API** - Lịch nhắc nhở
- **Google Cloud Vision** - Image processing
- **Aiven PostgreSQL** - Cloud database

## 📁 Cấu trúc thư mục

```
DAMH/
├── be/                         # Backend directory
│   └── hospital_web/          # Django project root
│       ├── api/               # API app
│       │   ├── migrations/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       │
│       ├── hospital/          # Templates directory
│       │   ├── admin_templates/
│       │   │   ├── admin_add_appointment.html
│       │   │   ├── admin_add_doctor.html
│       │   │   ├── admin_add_patient.html
│       │   │   ├── admin_approve_appointment.html
│       │   │   ├── admin_approve_doctor.html
│       │   │   ├── admin_approve_patient.html
│       │   │   ├── admin_dashboard.html
│       │   │   ├── admin_discharge_patient.html
│       │   │   ├── admin_doctor.html
│       │   │   ├── admin_patient.html
│       │   │   ├── admin_update_doctor.html
│       │   │   ├── admin_update_patient.html
│       │   │   ├── admin_view_appointment.html
│       │   │   ├── admin_view_doctor.html
│       │   │   ├── admin_view_doctor_specialisation.html
│       │   │   └── admin_view_patient.html
│       │   │
│       │   ├── doctor_templates/
│       │   │   ├── doctor_appointment.html
│       │   │   ├── doctor_dashboard.html
│       │   │   ├── doctor_delete_appointment.html
│       │   │   ├── doctor_patient.html
│       │   │   ├── doctor_view_appointment.html
│       │   │   ├── doctor_view_discharge_patient.html
│       │   │   ├── doctor_view_patient.html
│       │   │   └── doctor_wait_approval.html
│       │   │
│       │   ├── patient_templates/
│       │   │   ├── patient_appointment.html
│       │   │   ├── patient_dashboard.html
│       │   │   ├── patient_discharge.html
│       │   │   ├── patient_view_appointment.html
│       │   │   └── patient_wait_approval.html
│       │   │
│       │   ├── aboutus.html
│       │   ├── admin_base.html
│       │   ├── adminlogin.html
│       │   ├── adminsignup.html
│       │   ├── appointment.html
│       │   ├── base.html
│       │   ├── contactus.html
│       │   ├── doctor_base.html
│       │   ├── doctorlogin.html
│       │   ├── doctorsignup.html
│       │   ├── home.html
│       │   ├── index.html
│       │   ├── login.html
│       │   ├── navbar.html
│       │   ├── patient_base.html
│       │   ├── patient_profile.html
│       │   ├── patientlogin.html
│       │   ├── patientsignup.html
│       │   ├── test_result.html
│       │   └── upload_test_result.html
│       │
│       ├── hospitalManagement/  # Main app
│       │   ├── migrations/
│       │   ├── static/
│       │   │   ├── css/
│       │   │   ├── images/
│       │   │   └── js/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── forms.py
│       │   ├── meeting_views.py
│       │   ├── models.py
│       │   ├── payos_views.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       │
│       ├── media/             # User uploaded files
│       │   ├── profile_pics/
│       │   └── test_results/
│       │
│       ├── hospital_web/      # Project settings
│       │   ├── __init__.py
│       │   ├── asgi.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       │
│       ├── .env
│       ├── .gitignore
│       ├── db.sqlite3
│       ├── manage.py
│       └── requirements.txt
│
├── fe/                      # Frontend directory (if separate)
│   └── (frontend files)
│
├── docs/                    # Documentation
│   ├── api/
│   ├── deployment/
│   └── user-guide/
│
├── tests/                   # Additional tests
│   ├── integration/
│   └── unit/
│
├── .git/                    # Git repository
├── .gitignore              # Git ignore file
├── LICENSE                 # License file
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```

## 🚀 Cài đặt và Chạy

### Yêu cầu hệ thống
- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (nếu có frontend riêng)

### 1. Clone repository
```bash
git clone https://github.com/yourusername/iv-medical.git
cd iv-medical/be/hospital_web
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường
Tạo file `.env` trong thư mục `hospital_web/`:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-postgresql-url
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GEMINI_API_KEY=your-gemini-api-key
PAYOS_CLIENT_ID=your-payos-client-id
PAYOS_API_KEY=your-payos-api-key
PAYOS_CHECKSUM_KEY=your-payos-checksum-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
```

### 5. Setup database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Chạy server
```bash
python manage.py runserver
```

Truy cập http://localhost:8000

## 📊 Database Schema

### Các model chính:
- **CustomUser**: Tài khoản người dùng mở rộng
- **Doctor**: Thông tin bác sĩ
- **Patient**: Thông tin bệnh nhân
- **Service**: Dịch vụ y tế (lịch hẹn, xét nghiệm)
- **Appointment**: Cuộc hẹn khám
- **Medicine**: Thuốc
- **Prescription**: Đơn thuốc


## 🔌 API Endpoints

### Authentication
```
POST /api/token/              # Lấy JWT token
POST /api/token/refresh/      # Refresh token
POST /api/patient/register/   # Đăng ký bệnh nhân
```

### Doctors
```
GET  /api/doctors/           # Danh sách bác sĩ
GET  /api/doctors/{id}/      # Chi tiết bác sĩ
```

### Appointments
```
POST /api/book-appointment/{doctor_id}/  # Đặt lịch
GET  /api/patient/profile/               # Profile bệnh nhân
```

### AI Features
```
POST /api/chat/              # Chatbot AI
```

## 🤝 Đóng góp

https://docs.google.com/spreadsheets/d/1WHjiuY4fgUMsBKskFfWrQ4nhuX5jWF9kYpFMSTdWC9E/edit?gid=0#gid=0

## 📞 Liên hệ

- Email: 23520075@gm.uit.edu.vn

## 🎯 Tính năng sắp tới

- [ ] Mobile app với React Native
- [ ] Cải thiện độ chính xác khi chuẩn đoán bệnh với AI
- [ ] Hệ thống thông báo realtime
- [ ] Báo cáo và thống kê nâng cao
- [ ] Tích hợp với các thiết bị y tế IoT

---

⭐ **Star** repository này nếu bạn thấy hữu ích!
