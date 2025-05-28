import json
import requests

GEMINI_API_URL = "http://localhost:8000/api/chat/"

def call_gemini_api(message: str) -> str:
    try:
        response = requests.post(GEMINI_API_URL, json={"message": message})
        response.raise_for_status()
        return response.json().get("reply", "")
    except Exception as e:
        raise RuntimeError(f"Failed to communicate with Gemini API: {e}")

def process_medicine_description_with_gemini(description: str) -> dict:
    prompt = f"""
    Bạn là một trợ lý y tế. Hãy phân tích mô tả thuốc sau đây, sau đó:

    1. Dịch nội dung sang tiếng Việt.
    2. Tóm tắt mục đích và cách sử dụng.
    3. Ước tính số lần dùng thuốc mỗi ngày (times_per_day).
    4. Ước tính giá thuốc trung bình mỗi ngày bằng Việt Nam đồng (price).

    Trả về kết quả ở định dạng JSON như sau:
    {{
        "translated_summary": "<mô tả ngắn gọn đã dịch>",
        "times_per_day": <số nguyên>,
        "estimated_price": <số thực>
    }}

    Dưới đây là mô tả thuốc:
    \"\"\"{description}\"\"\"
    """

    reply = call_gemini_api(prompt)

    # Parse Gemini reply as JSON
    try:
        return json.loads(reply)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini trả về không đúng định dạng JSON:\n{reply}\nLỗi: {e}")
