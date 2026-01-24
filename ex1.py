import os
from dotenv import load_dotenv
from google import genai

# โหลดค่าจากไฟล์ .env
load_dotenv()

# ดึง Key มาเก็บในตัวแปร
my_key = os.getenv("GEMINI_API_KEY")

# ตรวจสอบเบื้องต้น (บรรทัดนี้ลบออกได้ถ้าทำงานได้แล้ว)
if my_key:
    print("✅ โหลด Key สำเร็จแล้วจ้า!")
else:
    print("❌ หา Key ไม่เจอ ตรวจสอบชื่อในไฟล์ .env อีกรอบนะ")

client = genai.Client(api_key=my_key)
