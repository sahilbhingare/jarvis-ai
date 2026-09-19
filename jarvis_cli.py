import os
import sys
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

from jarvis_actions import handle_action, get_current_time, get_system_status
from jarvis_brain import get_answer
from jarvis_voice import speak_sync

def main():
    print("=" * 60)
    print("   🤖 J.A.R.V.I.S. TERMINAL VOICE ASSISTANT")
    print("   (मराठी, English & Hindi Support)")
    print("   Type 'exit' or 'बाहेर पड' to quit.")
    print("=" * 60)

    # Initial greeting
    greeting = "नमस्कार सर! मी जार्व्हिस आहे. सर्व सिस्टीम्स ऑनलाईन आहेत. मी आपली काय मदत करू शकतो?"
    print(f"\n[JARVIS]: {greeting}")
    speak_sync(greeting, preferred_lang='mr')

    while True:
        try:
            user_input = input("\n[YOU]: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye', 'बाहेर पड', 'बंद कर']:
                farewell = "निरोप सर, काळजी घ्या! जय शिवराय!"
                print(f"[JARVIS]: {farewell}")
                speak_sync(farewell, preferred_lang='mr')
                break

            # Check action
            is_action, response = handle_action(user_input, lang='mr')
            if not is_action:
                # Query brain
                response = get_answer(user_input, lang='mr')

            print(f"\n[JARVIS]: {response}\n")
            speak_sync(response, preferred_lang='mr')

        except KeyboardInterrupt:
            print("\nShutting down Jarvis...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
