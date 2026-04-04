from speech_engine import speak, listen
from command_handler import process_command
from ai_module import generate_ai_response
from face_auth import authenticate_user, register_face
from gesture_control import run_gesture_control
import threading

def start_gesture_thread():
    thread = threading.Thread(target=run_gesture_control, daemon=True)
    thread.start()

def main():
    print("=" * 50)
    print("   AI Personal Voice Assistant - FRUIT")
    print("=" * 50)

    speak("Starting face authentication.")
    authenticated = authenticate_user()

    if not authenticated:
        speak("Face not recognized. Access denied.")
        print("Authentication failed.")
        return

    speak("Face recognized. Welcome!")
    speak("Personal voice assistant Fruit is now activated. How can I help you?")

    while True:
        try:
            command = listen()

            if not command:
                continue

            if "exit" in command or "stop" in command or "goodbye" in command:
                speak("Goodbye! Have a great day.")
                break

            elif "register face" in command:
                speak("What is the name for this face?")
                name = listen()
                if name:
                    register_face(name)
                    speak(f"Face registered for {name}.")

            elif "gesture mode" in command or "gesture control" in command:
                speak("Starting gesture control mode. Press ESC to stop.")
                start_gesture_thread()

            else:
                response = process_command(command)
                if response:
                    speak(response)
                else:
                    ai_response = generate_ai_response(command)
                    speak(ai_response)

        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()