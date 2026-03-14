import pygame
import asyncio
import os
from gradio_client import Client

# --- 1. เชื่อมต่อ Server ครั้งเดียว (อยู่นอกฟังก์ชันเพื่อความเร็ว) ---
print("🔌 กำลังเชื่อมต่อกับ Moe TTS...")
try:
    client = Client("Moe-tts/")
    print("✅ เชื่อมต่อสำเร็จ!")
except Exception as e:
    print(f"❌ เชื่อมต่อไม่ได้: {e}")
    client = None

async def speak(text):
    if client is None:
        print("⚠️ ระบบเสียงไม่พร้อม: ไม่ได้เชื่อมต่อกับ Server")
        return

    print(f"🗣️ ฟ้าใสกำลังส่งเสียง: {text}")
    
    try:
        # --- 2. ส่งคำพูดไปให้น้องโม่ย (ใช้ชื่อโมเดลและ API ที่คุณพิงทดสอบแล้วผ่าน) ---
        result = client.predict(
            text=text,           # ข้อความจาก brain.py
            speaker="ATRI",    # ชื่อตัวละครที่คุณพิงทดสอบแล้วได้ไฟล์
            speed=1,
            is_symbol=False,
            api_name="/tts_fn_7"  # API Name ตัวล่าสุดที่คุณพิงส่งมา
        )
        
        # --- 3. แกะ Tuple 'Success' เพื่อเอา Path ไฟล์เสียง ---
        # ผลลัพธ์คือ ('Success', 'C:\\...\\audio.wav') เราจะเอาตัวที่ 2
        if isinstance(result, (list, tuple)) and len(result) > 1:
            OUTPUT_FILE = result[1] 
        else:
            OUTPUT_FILE = result
            
        print(f"📁 เจอไฟล์เสียงที่: {OUTPUT_FILE}")

        # --- 4. เล่นเสียงด้วย pygame ---
        if OUTPUT_FILE and os.path.exists(OUTPUT_FILE):
            pygame.mixer.init()
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            
            # รอจนกว่าจะพูดจบ
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            pygame.mixer.quit()
        else:
            print("ระบบหาไฟล์เสียงไม่เจอ")

    except Exception as e:
        print(f" เกิดข้อผิดพลาดในระบบเสียง: {e}")