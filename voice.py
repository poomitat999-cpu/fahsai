import pygame
import asyncio
import os
import contextlib
from gradio_client import Client
from dotenv import load_dotenv

<<<<<<< HEAD
load_dotenv()
TTS_URL = os.getenv("Moe_tts")
client = None

if TTS_URL:
    try:
        with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
            client = Client(TTS_URL)
            
    except Exception:
       
        client = None
=======
# --- 1. เชื่อมต่อ Server ครั้งเดียว (อยู่นอกฟังก์ชันเพื่อความเร็ว) ---
print("🔌 กำลังเชื่อมต่อกับ Moe TTS...")
try:
    load_dotenv()
    TTS_URL = os.getenv("Moe_tts")
    print("✅ เชื่อมต่อสำเร็จ!")
except Exception as e:
    print(f"❌ เชื่อมต่อไม่ได้: {e}")
    client = None
>>>>>>> c3f497d452e11128ea59a67bcd563743bc010654

async def speak(text):
    if client is None:
        return 
    
    try:

        result = client.predict(
            text=text,           
            speaker="ATRI",    
            speed=1,
            is_symbol=False,
            api_name="/tts_fn_7"  
        )

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
