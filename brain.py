import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MEMORY_FILE = "fahsai_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"user_name": "คุณพิง", "monster_count": 0, "status": "เพื่อนสนิท"}

def save_memory(data):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- (เพิ่มใหม่) ฟังก์ชันสำหรับแยกอารมณ์ออกจากข้อความ ---
def parse_emotion(raw_text):
    if "|" in raw_text:
        parts = raw_text.split("|")
        # เอา [ ] ออกจากอารมณ์
        emotion = parts[0].replace("[", "").replace("]", "").strip()
        message = parts[1].strip()
        return emotion, message
    return "ปกติ", raw_text # ถ้าไม่มีรูปแบบ ให้เป็นอารมณ์ปกติ

def get_response(user_input, user_data):
    # --- (ปรับปรุง) ใส่คำสั่งเรื่องอารมณ์ลงใน Instruction ---
    instruction = (
        f"คุณคือฟ้าใส AI VTuber ร่าเริง เจ้านายชื่อ {user_data['user_name']} "
        f"ดื่ม Monster ไป {user_data['monster_count']} กระป๋อง "
        "ทุกครั้งที่ตอบ ให้เลือก 1 อารมณ์จาก [ปกติ, ดีใจ, เศร้า, โกรธ, ตกใจ] "
        "และต้องตอบในรูปแบบ [อารมณ์]|ข้อความ เท่านั้น"
    )

    chat = client.chats.create(
        model="gemini-2.5-flash", # ปรับเป็นรุ่นปัจจุบันที่เสถียรครับ
        config={'system_instruction': instruction}
    )
    
    response = chat.send_message(user_input)
    
    # --- (เพิ่มใหม่) แยกอารมณ์ก่อนส่งคืน ---
    emotion, clean_message = parse_emotion(response.text)
    return emotion, clean_message

# --- ตัวอย่างการรัน (เอาไปลองใน Terminal) ---

if __name__ == "__main__":
    current_user = load_memory()
    print(f"--- ฟ้าใส Online (โหมดมีอารมณ์) ---")
    print(f"สถานะปัจจุบัน: ดื่ม Monster ไป {current_user['monster_count']} กระป๋อง")
    
    while True:
        text = input(f"{current_user['user_name']}: ")
        if text.lower() == "exit": 
            print("บ๊ายบายค่ะเจ้านาย!")
            break
        
        # ส่งไปให้ Gemini คิดคำตอบ
        emo, msg = get_response(text, current_user)
        
        # --- [ตัวอย่างการอัปเดตข้อมูล] ---
        # สมมติว่าถ้าเราคุยเรื่อง Monster ให้ลองเพิ่มจำนวนใน memory ดู
        if "monster" in text.lower() or "มอนสเตอร์" in text:
            current_user['monster_count'] += 1
            print(f"✨ (บันทึกข้อมูล: ดื่มเพิ่มเป็น {current_user['monster_count']} กระป๋อง)")

        # --- [จุดสำคัญ] สั่งบันทึกไฟล์ทันทีหลังจากข้อมูลเปลี่ยน ---
        save_memory(current_user)
        
        print(f"--- [Status: {emo}] ---")
        print(f"ฟ้าใส: {msg}\n")