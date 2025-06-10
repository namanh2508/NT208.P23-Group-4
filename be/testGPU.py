import torch

# Lệnh quan trọng nhất: Kiểm tra xem CUDA có sẵn sàng không
is_available = torch.cuda.is_available()
print(f"CUDA Available: {is_available}")

if is_available:
    # Lấy số lượng GPU
    device_count = torch.cuda.device_count()
    print(f"Number of GPUs: {device_count}")

    # Lấy tên của GPU đầu tiên (device 0)
    gpu_name = torch.cuda.get_device_name(0)
    print(f"GPU Name: {gpu_name}")