import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# 1. ตั้งค่า API
client = genai.Client(api_key=api_key)

# 2. สร้าง Chat Session 
chat_session = client.chats.create(model="models/gemini-2.5-flash")

print("--- 'ฟ้าใส' โหมดความจำสมบูรณ์ พร้อมคุยกับคุณพิงแล้ว ---")
print("(พิมพ์ 'exit' เพื่อปิดโปรแกรม)")

while True:
    user_input = input("คุณพิง: ")
    
    ''
    if user_input.lower() == 'exit':
        print("ฟ้าใส: บ๊ายบายค่ะคุณพิง!")
        break
        
    try:
        # เปลี่ยนจาก generate_content เป็น chat_session.send_message
        # เพื่อให้มันส่งประวัติการคุย (History) กลับไปด้วยทุกครั้ง
        response = chat_session.send_message(user_input)
        
        print(f"✨ ฟ้าใส: {response.text}")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")