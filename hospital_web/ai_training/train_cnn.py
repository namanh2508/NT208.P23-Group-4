# # ai_training/train_cnn.py

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torchvision import datasets, transforms
# from torch.utils.data import DataLoader
# import os

# # --- 1. Định nghĩa model CNN ---
# class CNNmodel(nn.Module):
#     def __init__(self, num_classes=3):
#         super(CNNmodel, self).__init__()
#         self.conv1 = nn.Conv2d(3, 32, kernel_size=3)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
#         self.fc1 = nn.Linear(64 * 30 * 30, 128)
#         self.fc2 = nn.Linear(128, num_classes)

#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = x.view(-1, 64 * 30 * 30)
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return x

# # --- 2. Load data ---
# transform = transforms.Compose([
#     transforms.Resize((128, 128)),
#     transforms.ToTensor(),
# ])

# import os

# dataset_path = os.path.join(os.path.dirname(__file__), "dataset")  # thư mục chứa ảnh đã phân loại
# dataset = datasets.ImageFolder(dataset_path, transform=transform)
# loader = DataLoader(dataset, batch_size=16, shuffle=True)

# # Lưu tên lớp để sau này predict
# labels = dataset.classes
# with open("labels.txt", "w") as f:
#     for label in labels:
#         f.write(label + "\n")

# # --- 3. Khởi tạo model ---
# model = CNNmodel(num_classes=len(labels))
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# criterion = nn.CrossEntropyLoss()

# # --- 4. Train ---
# for epoch in range(10):
#     for images, labels in loader:
#         outputs = model(images)
#         loss = criterion(outputs, labels)

#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#     print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# # --- 5. Lưu model ---
# torch.save(model.state_dict(), "../hospitalManagement/ai_models/cnn_model.pth") # Model saved to hospitalManagement/ai_models/cnn_model.pth

