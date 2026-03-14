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

def get_response(user_input, user_data):
    instruction = f"คุณคือฟ้าใส AI ร่าเริง เจ้านายชื่อ {user_data['user_name']} ดื่ม Monster ไป {user_data['monster_count']} กระป๋อง"

    # สร้างการสนทนา
    chat = client.chats.create(
        model="models/gemini-2.5-flash",
        config={'system_instruction': instruction}
    )
    response = chat.send_message(user_input)
    return response.text