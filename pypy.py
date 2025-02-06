import pyautogui
import time
import pyperclip
import google.generativeai as genai

# Configure the API
genai.configure(api_key="AIzaSyBX6r9tX8Kmsjph68lmb1uD8FU8FD9rSNE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Click on the Opera icon at (649, 737)
pyautogui.click(649, 737)  # Opera icon
time.sleep(1)  # Wait for the application to open

# Click and drag to select text
pyautogui.moveTo(544, 164)
pyautogui.mouseDown()
pyautogui.moveTo(1314, 636, duration=1)  # Smooth drag
pyautogui.mouseUp()

# Copy the selected text (Ctrl+C)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)  # Wait for the clipboard to update

# Get the copied text
chat_history = pyperclip.paste()

# Create messages structure for the AI model
messages = [
    {"role": "system", "content": "You are a person named Muavia who speaks Urdu as well as English. He is from Pakistan and is a student and class representative of class. You have to analyze chat history and talk and respond like Muavia"},
    {"role": "user", "content": chat_history}
]

# Generate the response using the chat history
response = model.generate_content(messages)  # Pass the entire messages list

# Move to the position and click the chat input box
pyautogui.click(1147, 695)

# Wait a bit for the system to be ready
time.sleep(1)

# Copy the response to the clipboard
pyperclip.copy(response['content'])  # Extract the response content

# Paste the text from the clipboard
pyautogui.hotkey('ctrl', 'v')

# Wait a moment before pressing Enter
time.sleep(1)

# Press Enter to send the message
pyautogui.press('enter')
