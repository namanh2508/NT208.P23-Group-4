# ***HỆ THỐNG CHĂM SÓC SỨC KHỎE THÔNG MINH***
## **I. Tổng Quan**
### **1. Giới thiệu đề tài** 
Đồ án Hệ thống chăm sóc sức khỏe thông minh là một giải pháp công nghệ giúp tối ưu hóa quy trình khám chữa bệnh, nâng cao chất lượng dịch vụ y tế và hỗ trợ bác sĩ trong chẩn đoán, điều trị. Hệ thống ứng dụng các công nghệ như hồ sơ sức khỏe điện tử và các công cụ hỗ trợ chẩn đoán để nâng cao hiệu quả chăm sóc sức khỏe.
### **2. Mục tiêu đề tài** 
- Tối ưu quy trình khám chữa bệnh: Giảm thời gian chờ, đơn giản hóa thủ tục.

- Hỗ trợ chẩn đoán và điều trị: Cung cấp công cụ phân tích dữ liệu y tế giúp bác sĩ đưa ra quyết định chính xác hơn.

- Tăng cường quản lý sức khỏe cá nhân: Ứng dụng theo dõi sức khỏe, nhắc lịch khám, gợi ý lối sống lành mạnh.

- Kết nối hệ thống y tế: Liên kết dữ liệu giữa bệnh viện, phòng khám, bảo hiểm y tế để tạo ra một hệ sinh thái thống nhất.
### **3. Các tính năng chính của đề tài**
✔️ Đặt lịch khám trực tuyến, trực tiếp 

✔️ Theo dõi hồ sơ bệnh án   

✔️ Nhận tư vấn từ bác sĩ 

✔️ Nhắc nhở uống thuốc, tập luyện

✔️ Hỗ trợ bác sĩ trong chẩn đoán thông qua hình ảnh hoặc triệu chứng 

## **II. Hệ Thống**
### **1. Công nghệ sử dụng**
✅ **Backend:** Django, Django REST Framework 

✅ **Frontend:** React.js 

✅ **Database:** PostgreSQL  
### **2. Yêu cầu hệ thống**  
| Thành phần    | Phiên bản đề xuất |
|--------------|----------------|
| Python      | 3.13+           |
| PostgreSQL  | 17+            |
| Docker      | Latest         |
### **3. Phân tích thiết kế hệ thống** 
![HospitalSystem](https://github.com/user-attachments/assets/6a956335-1982-48e8-8672-a5b4ed353b27)
### **4. Mô tả Thành phần (Component Descriptions)** 


*   **Users (Người dùng):**
    
    *   `Web Application`: Giao diện web cho bệnh nhân, bác sĩ, và quản trị viên.
      
    *   `Mobile Application`: Ứng dụng di động cho bệnh nhân và bác sĩ (tùy chọn).
      
*   **Gateways (Cổng Giao tiếp):**
  
    *   `API Gateway`: Điểm vào duy nhất cho tất cả yêu cầu từ client. Xử lý routing, xác thực cơ bản, rate limiting, v.v.
*   **Core Services (Dịch vụ Cốt lõi):**
  
    *   `Auth Service`: Quản lý định danh, xác thực (login/signup), phân quyền và quản lý phiên làm việc (tokens).
      
    *   `Appointment Service`: Xử lý việc đặt lịch hẹn, quản lý lịch làm việc của bác sĩ, gửi nhắc nhở.
      
    *   `EHR Service (Electronic Health Record)`: Dịch vụ quan trọng nhất, lưu trữ và quản lý hồ sơ bệnh án điện tử chi tiết (lịch sử khám, xét nghiệm, chẩn đoán, dị ứng, v.v.).
      
    *   `Consultation Service`: Hỗ trợ các phiên tư vấn trực tuyến, kết nối tới dịch vụ video.
      
    *   `Prescription Service`: Quản lý việc tạo, xem và cấp phát đơn thuốc điện tử (e-prescription).
    *   `Billing Service`: Xử lý tạo hóa đơn, tích hợp cổng thanh toán, quản lý lịch sử giao dịch.
      
    *   `Notification Service`: Gửi thông báo (email, SMS, push notification) đến người dùng dựa trên các sự kiện (lịch hẹn, đơn thuốc mới, v.v.).
      
*   **Infrastructure (Cơ sở Hạ tầng):**
    *   `Databases`: Có thể bao gồm nhiều loại CSDL:
        *   *Relational (PostgreSQL):* Cho dữ liệu có cấu trúc (người dùng, lịch hẹn, hóa đơn).
          
    *   `Message Queue`: (RabbitMQ, Kafka, SQS, etc.) Dùng để giao tiếp bất đồng bộ giữa các services, giảm tải và tăng độ tin cậy (ví dụ: khi đặt lịch hẹn thành công, gửi message để Notification Service gửi email).
  
    *   `Search Engine`: Cung cấp khả năng tìm kiếm nhanh chóng và phức tạp trên dữ liệu lớn
  
*   **External Services (Dịch vụ Bên ngoài):**
    *   `Payment Gateway`: Tích hợp với các nhà cung cấp dịch vụ thanh toán.
    *   `Video Conferencing Service`: Dịch vụ cung cấp hạ tầng video call
    *   `SMS/Email Gateway`: Dịch vụ gửi SMS và Email.

### **5. Luồng dữ liệu chính (Key Data Flows)**

*   **Đặt lịch hẹn:** Client -> API Gateway -> Appointment Service -> Database
  
*   **Xem hồ sơ bệnh án:** Client -> API Gateway -> EHR Service -> Database
  
*   **Tư vấn từ xa:** Client -> API Gateway -> Appointment Service -> Video Service
  
*   **Thanh toán:** Client -> API Gateway -> Billing Service -> Payment Gateway

*   **Xem thông tin thuốc** Client -> External API

*   **Nhắc nhở tập luyện** Client -> API Gateway -> Database -> Google Calendar API
