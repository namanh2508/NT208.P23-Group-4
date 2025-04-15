import torch
from torchvision import transforms
from PIL import Image
from hospital_web.ai_training import CNNmodel  # mô hình CNN bạn đã định nghĩa

# Load mô hình đã train
model = CNNmodel(num_classes=3)
model.load_state_dict(torch.load('hospitalManagement/ai_models/cnn_model.pth', map_location='cpu'))
model.eval()  # Đặt model ở chế độ dự đoán (inference)

# Load danh sách lớp từ file labels.txt
with open('hospitalManagement/ai_models/labels.txt', 'r') as f:
    class_names = [line.strip() for line in f.readlines()]
# class_names = ['lab_report', 'dermatology', 'xray']

# Tiền xử lý ảnh giống lúc train
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])

# 🔮 Hàm dự đoán ảnh mới
def detect_record_type_by_cnn(image_path):
    image = Image.open(image_path).convert('RGB')  # mở ảnh
    image = transform(image).unsqueeze(0)  # thêm batch dimension: [1, 3, 128, 128]

    with torch.no_grad():  # không cần gradient khi dự đoán
        outputs = model(image)              # chạy qua mạng
        _, predicted = torch.max(outputs, 1)  # lấy index class lớn nhất
        return class_names[predicted.item()]  # trả về tên lớp