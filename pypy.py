import pyautogui
import time
import pyperclip
import google.generativeai as genai

sender_name = "Mama"

# API key (Never expose API keys publicly)
api_key = "api key

# Configure the API
genai.configure(api_key=api_key)

pyautogui.click(649, 737)
time.sleep(2)

def get_chat_history():
    """Extracts the full chat history only once at the start."""
    pyautogui.click(562, 167)  # Click on chat area
    time.sleep(1)

    pyautogui.mouseDown()
    pyautogui.moveTo(1081, 615, duration=1)  # Drag to select text
    pyautogui.mouseUp()

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)  # Ensure clipboard updates

    return pyperclip.paste().strip()

def get_last_message(chat_log, sender_name="Mama"):
    """Extracts the last message from the given chat log."""
    messages = chat_log.strip().split("\n")
    last_message = None

    for msg in reversed(messages):
        if sender_name in msg:
            last_message = msg.split(":", 1)[-1].strip()
            break

    return last_message

def is_last_message_from_sender(chat_log, sender_name="Mama"):
    """Checks if the last message in the chat history is from the sender."""
    messages = chat_log.strip().split("/2024]")[-1]  # Get last timestamped section
    return sender_name in messages

# Step 1: Extract Full Chat History First
full_chat_history = get_chat_history()
print("Full Chat History:\n", full_chat_history)

# Step 2: Start Checking Only the Last Message
while True:
    # Step 2a: Extract only the latest message
    last_message = get_last_message(full_chat_history, sender_name)
    
    if last_message:
        print(f"{sender_name} asked: {last_message}")
    else:
        print(f"No message found from {sender_name}.")
    
    # Step 2b: Check if the last message is from Mama
    if is_last_message_from_sender(full_chat_history):
        print(f"Last message is from {sender_name}.")

        # Create a response prompt
        prompt_text = f"""
        Bro, tu Muavia hai jo doston aur family (Mama, Papa) se Urdu-English mix mai baat kar raha hai.  
        Baatein natural rakhni hain, koi formality nahi.  
        Sirf 1-2 lines ka short aur direct reply dena.  
        Khud se topic change karna, lekin overthink nahi.  
        Ab Muavia ki tarah short aur relaxed reply kar! (Do not use 'chill' more than once)
        """
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate response
        response = model.generate_content([{"role": "user", "parts": [prompt_text]}])
        response_text = response.text.strip() if response and response.text else "Error: No response from Gemini."

        # Copy response to clipboard
        pyperclip.copy(response_text)

        # Move to message input box and paste the response
        pyautogui.click(1147, 695)
        time.sleep(1)

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        print("Response Sent:", response_text)

    else:
        print(f"Last message is NOT from {sender_name}.")

    # Delay before the next loop iteration
    time.sleep(5)
