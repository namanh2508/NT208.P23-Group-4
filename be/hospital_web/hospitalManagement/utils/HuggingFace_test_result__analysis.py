import requests
from django.conf import settings

import requests

def analyze_lab_result(ocr_text, model='phi3'):
    try:
        prompt = (
            "Hãy phân tích kết quả xét nghiệm sau và cho biết tình trạng sức khỏe của bệnh nhân. "
            
            f"{ocr_text}"
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "Không có phản hồi từ mô hình.")
    
    except Exception as e:
        return f"Lỗi khi kết nối Ollama: {e}"