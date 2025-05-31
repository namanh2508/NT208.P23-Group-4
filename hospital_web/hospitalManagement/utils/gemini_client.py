import json
import google.generativeai as genai

# Configure Gemini SDK once at import
genai.configure(api_key="AIzaSyCyJiVy8beS2XiDEBz7vosPP5Sh65yp5zU")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def process_medicine_description_with_gemini(usage: str, description: str) -> dict:
    """
    Sends a prompt to Gemini to translate, summarize, and estimate dosage and price.
    Returns a dict with keys: translated_summary (str), times_per_day (int), estimated_price (float)
    """
    prompt = (
        "Bạn là một trợ lý y tế. Hãy phân tích mô tả thuốc sau đây, sau đó:"
        "1. Dịch nội dung sang tiếng Việt."
        "2. Tóm tắt mục đích và cách sử dụng."
        "3. Ước tính số lần dùng thuốc mỗi ngày (times_per_day) dựa trên công dụng và chỉ định thuốc, ngay cả khi thông tin không đầy đủ."
        "4. Ước tính giá thuốc trung bình mỗi viên bằng Việt Nam đồng (price) dựa trên giá thị trường ước tính."
        "**QUAN TRỌNG**: Luôn trả về KẾT QUẢ DUY NHẤT ở định dạng JSON theo mẫu dưới đây, không có bất kỳ chú thích nào khác bên ngoài JSON:"
        "Trả về kết quả ở định dạng JSON như sau:"
        "{"
        "    \"translated_summary\": \"<mô tả chức năng thuốc ngắn gọn, dưới 100 chữ cái, đã dịch>\","
        "    \"times_per_day\": <số nguyên>,"
        "    \"estimated_price\": <số thực>"
        "}"
        f"Dưới đây là mô tả thuốc:{description}"
        f"Dưới đây là công dụng và chỉ định thuốc:{usage}"
    )
    response = model.generate_content([prompt])
    text = getattr(response, 'text', None)
    # Remove markdown code fences if present
    if text.startswith("```"):
        # strip fences
        # remove leading ```json or ```
        lines = text.splitlines()
        # filter out lines that are exactly code fence markers
        cleaned = []
        for line in lines:
            if line.strip().startswith('```'):
                continue
            cleaned.append(line)
        text = ''.join(cleaned).strip()
    if text is None:
        raise RuntimeError("No text returned from Gemini response")

    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        # Raise with full text content for debugging
        raise ValueError(f"Gemini returned invalid JSON:{text} Error: {e}")

    # Validate keys
    for key in ("translated_summary", "times_per_day", "estimated_price"):
        if key not in result:
            raise KeyError(f"Missing '{key}' in Gemini response")

    return result
