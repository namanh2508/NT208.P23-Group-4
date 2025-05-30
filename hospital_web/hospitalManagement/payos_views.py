from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from payos import PayOS, ItemData, PaymentData
import time
import json
from .models import AI_Metric, Doctor,Patient,Appointment,Service
from hospitalManagement import models
TEMP_PAYOS_CLIENT_ID = "c387c8ae-5f34-4aea-b098-d0f2851064ea"
TEMP_PAYOS_API_KEY = "211b8012-101c-4dc9-8f87-1392c037f207"
TEMP_PAYOS_CHECKSUM_KEY = "91161e3e498f0fc8928a80bca4bbe491933816bb2e330e251decb2fd9a7758f9"

payos_instance = PayOS(
    client_id=TEMP_PAYOS_CLIENT_ID,
    api_key=TEMP_PAYOS_API_KEY,
    checksum_key=TEMP_PAYOS_CHECKSUM_KEY
)
MY_DOMAIN = 'http://127.0.0.1:8000'
TEMP_PAYOS_RETURN_URL = '/' 
TEMP_PAYOS_CANCEL_URL = '/'

def create_payment_view(request, id):
    try:
        current_user = request.user
        des = f"BN {current_user.get_full_name()}"
        if len(des) > 25:
            des = f"BN {current_user.first_name}"
        
        print(f"Đang xử lý appointment với id: {id}")
        # Kiểm tra xem có bao nhiêu appointment với id này
        appointments = models.Appointment.objects.filter(id=id)
        print(f"Số lượng appointment tìm thấy: {appointments.count()}")
        for app in appointments:
            print(f"Appointment ID: {app.id}, Service: {app.service}, Status: {app.status}")
        
        my_appointment = models.Appointment.objects.get(id=id)
        print(f"Appointment được chọn: ID={my_appointment.id}, Service={my_appointment.service}")
        
        item = ItemData(name="Phí khám bệnh", quantity=1, price=2000)
        payment_data = PaymentData(
            orderCode=int(time.time()),
            amount=2000,
            description=des,
            items=[item],
            cancelUrl=MY_DOMAIN + '/cancel', 
            returnUrl=MY_DOMAIN + "/success", 
        )
        print(f"OrderCode mới: {payment_data.orderCode}")
        
        # Kiểm tra trước khi cập nhật
        print(f"OrderCode cũ: {my_appointment.orderCode}")
        models.Appointment.objects.filter(id=id).update(orderCode=payment_data.orderCode)
        print(f"Đã cập nhật orderCode thành công")
        
        payment_link_response = payos_instance.createPaymentLink(payment_data) 
        return redirect(payment_link_response.checkoutUrl)
    except Exception as e:
        print(f"Lỗi khi tạo link thanh toán PayOS: {e}")
        return HttpResponse(f"Có lỗi xảy ra trong quá trình tạo thanh toán: {str(e)}", status=500)
    

def success_view(request):
    current_user = request.user
    return render(request, 'success.html', {'current_user': current_user}) 

def cancel_view(request):
    current_user = request.user
    return render(request, 'cancel.html', {'current_user': current_user})

@csrf_exempt
def receive_webhook_view(request):
    if request.method == 'POST':
        try:
            webhook_data_received = json.loads(request.body)
            verified_data = payos_instance.verifyPaymentWebhookData(webhook_data_received)
            print("--- Webhook NHẬN ĐƯỢC tại /receive-webhook/ (Dữ liệu gốc) ---")
            print(f"Đối tượng verified_data (dạng str): {str(verified_data)}")
            if str(verified_data):
                if str(verified_data.desc) == 'success':
                    order_code = str(verified_data.orderCode)
                    print(order_code)
                    if order_code:
                        models.Appointment.objects.filter(orderCode=order_code).update(status='accepted')
                
            return JsonResponse({'message': 'Webhook received by Django. Raw data logged.'}, status=200)

        except json.JSONDecodeError:
            print("Webhook Lỗi (/receive-webhook/): Dữ liệu JSON không hợp lệ.")
            return JsonResponse({'error': 'Invalid JSON data provided'}, status=400)
        except Exception as e:
            # Bắt các lỗi chung khác nếu có trong quá trình cơ bản này
            print(f"Lỗi không xác định khi xử lý Webhook tại /receive-webhook/: {str(e)}")
            import traceback
            traceback.print_exc() # In traceback đầy đủ ra console server
            return JsonResponse({'error': f'Could not process raw webhook: {str(e)}'}, status=500) 
    
    # Nếu request không phải là POST
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed for this webhook.'}, status=405)