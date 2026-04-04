import datetime
import wikipedia
import pyautogui
import webbrowser
import os
from time import sleep
from screen_reader import read_screen

def process_command(command):

    if "time" in command:
        return "The time is " + datetime.datetime.now().strftime("%I:%M %p")

    elif "date" in command:
        return "Today is " + datetime.datetime.now().strftime("%B %d, %Y")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        if not topic:
            return "Please tell me what to search on Wikipedia."
        try:
            wikipedia.set_lang("en")
            result = wikipedia.summary(topic, sentences=2, auto_suggest=True)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                result = wikipedia.summary(e.options[0], sentences=2)
                return result
            except:
                return f"Multiple results found for {topic}. Please be more specific."
        except wikipedia.exceptions.PageError:
            return f"I could not find any Wikipedia page for {topic}."
        except Exception:
            return "I could not find that on Wikipedia."

    elif "open chrome" in command:
        pyautogui.press("win")
        sleep(1)
        pyautogui.write("chrome")
        sleep(0.5)
        pyautogui.press("enter")
        return "Opening Chrome."

    elif "open notepad" in command:
        pyautogui.press("win")
        sleep(1)
        pyautogui.write("notepad")
        sleep(0.5)
        pyautogui.press("enter")
        return "Opening Notepad."

    elif "open vs code" in command:
        pyautogui.press("win")
        sleep(1)
        pyautogui.write("visual studio code")
        sleep(0.5)
        pyautogui.press("enter")
        return "Opening VS Code."

    elif "open calculator" in command:
        pyautogui.press("win")
        sleep(1)
        pyautogui.write("calculator")
        sleep(0.5)
        pyautogui.press("enter")
        return "Opening Calculator."
    
    elif "open spotify" in command:
        pyautogui.press("win")
        sleep(1)
        pyautogui.write("spotify")
        sleep(0.5)
        pyautogui.press("enter")
        sleep(3)
        return "Opening Spotify."

    elif ("play" in command and "music" in command) or ("play" in command and "song" in command) or "resume music" in command or command.strip() == "play":
        pyautogui.press("playpause")
        return "Playing music."

    elif "pause" in command or "stop music" in command or "stop song" in command or "stop playing" in command:
        pyautogui.press("playpause")
        return "Music paused."

    elif "next song" in command or "next track" in command:
        pyautogui.press("nexttrack")
        return "Playing next song."

    elif "previous song" in command or "previous track" in command:
        pyautogui.press("prevtrack")
        return "Playing previous song."

    elif "play tamil" in command or "play english" in command or "play hindi" in command:
        if "tamil" in command:
            search_term = "tamil hits"
        elif "hindi" in command:
            search_term = "hindi hits"
        else:
            search_term = "english hits"
        import webbrowser
        webbrowser.open(f"https://open.spotify.com/search/{search_term}")
        return f"Searching Spotify for {search_term}."

    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query}."
        return "What should I search for?"

    elif "close window" in command:
        pyautogui.hotkey("alt", "f4")
        return "Closing the window."

    elif "volume up" in command:
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Volume increased."

    elif "volume down" in command:
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Volume decreased."

    elif "mute" in command:
        pyautogui.press("volumemute")
        return "Muted."

    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved."

    elif "lock" in command:
        pyautogui.hotkey("win", "l")
        return "Locking the computer."

    elif command.startswith("type "):
        text = command[5:]
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"
    
    elif "read screen" in command or "read my screen" in command or "what is on screen" in command:
        result = read_screen()
        # Clean the text for speaking
        import re
        result = re.sub(r'[^\w\s.,]', '', result)
        result = ' '.join(result.split())
        if len(result) > 200:
            return result[:200] + ". There is more text on screen."
        if not result.strip():
            return "I could not find any readable text on screen."
        return result

    else:
        return None