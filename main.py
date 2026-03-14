# main.py
import asyncio
import brain
import voice

def main():
    print("--- ⚡️ ฟ้าใส ออนไลน์! ---")
    user_data = brain.load_memory()

    while True:
        user_input = input(f"{user_data['user_name']}: ")
        
        if user_input.lower() in ['exit', 'quit']:
            brain.save_memory(user_data)
            break
            
        # 1. ส่งให้สมองคิด
        response_text = brain.get_response(user_input, user_data)
        print(f"✨ ฟ้าใส: {response_text}")
        
        # 2. ส่งให้กล่องเสียงพูด (ทำแบบขนาน)
        asyncio.run(voice.speak(response_text))

if __name__ == "__main__":
    main()
