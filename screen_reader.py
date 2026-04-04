import pytesseract
import pyautogui
from PIL import Image
import os

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_screen():
    """Takes a screenshot and reads all text on screen"""
    try:
        print("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot.save("temp_screen.png")

        image = Image.open("temp_screen.png")
        text = pytesseract.image_to_string(image)

        # Clean up temp file
        os.remove("temp_screen.png")

        if text.strip():
            return text.strip()
        else:
            return "I could not find any text on the screen."

    except Exception as e:
        print(f"Screen reader error: {e}")
        return "Sorry, I could not read the screen."

def read_selected_area(x, y, width, height):
    """Reads text from a specific area of screen"""
    try:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        text = pytesseract.image_to_string(screenshot)

        if text.strip():
            return text.strip()
        else:
            return "No text found in that area."

    except Exception as e:
        return "Could not read that area."