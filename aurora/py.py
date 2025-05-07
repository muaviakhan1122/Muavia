import pyautogui
import time
import pyperclip
import google.generativeai as genai
from datetime import datetime
import re
import random

# Configure WhatsApp
WHATSAPP_POSITIONS = {
    'chat_area': (562, 167),
    'input_box': (1147, 695),
    'send_button': (649, 737)
}

# Configure AI
genai.configure(api_key="AIzaSyBygYbUpztuT76GkpEigtIelEX_nJRBAkg")
model = genai.GenerativeModel("gemini-1.5-flash")

class WhatsAppAutoReplier:
    def __init__(self, sender_name="Mama"):
        self.sender_name = sender_name
        self.last_message_time = None
        self.conversation_context = []
        self.response_style = "casual"
        self.language_preference = "urdu-english"  # Can be 'urdu', 'english', or 'urdu-english'
        self.last_interaction_type = None
        self.message_history = []
        
    def get_chat_history(self):
        """Extracts the full chat history with improved reliability"""
        try:
            # Click on chat area with error handling
            self.safe_click(*WHATSAPP_POSITIONS['chat_area'])
            time.sleep(1.5)
            
            # Select text more reliably
            pyautogui.mouseDown()
            pyautogui.moveTo(1081, 615, duration=0.5)
            pyautogui.mouseUp()
            
            # Copy to clipboard with retry logic
            for _ in range(3):
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.5)
                clipboard_content = pyperclip.paste().strip()
                if clipboard_content:
                    return clipboard_content
            
            return ""
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return ""

    def safe_click(self, x, y, clicks=1):
        """Click with safety checks"""
        try:
            # Save current mouse position
            original_pos = pyautogui.position()
            
            # Move and click
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click(clicks=clicks)
            
            # Return to original position
            pyautogui.moveTo(original_pos, duration=0.3)
        except Exception as e:
            print(f"Click error: {e}")

    def extract_last_message(self, chat_log):
        """Improved message extraction with regex and context awareness"""
        if not chat_log:
            return None, None
        
        # Split messages by timestamp pattern (adjust based on your WhatsApp language)
        messages = re.split(r'\n(?=\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[AP]M - )', chat_log)
        
        if not messages:
            return None, None
            
        # Get the last message
        last_msg = messages[-1].strip()
        
        # Extract sender and content
        sender_match = re.match(r'^(.+?):', last_msg)
        if sender_match:
            sender = sender_match.group(1)
            content = last_msg[len(sender)+1:].strip()
            return sender, content
            
        return None, last_msg

    def is_new_message(self, current_message):
        """Check if this is a new message we haven't processed"""
        if not current_message:
            return False
            
        # Check against message history
        if current_message in self.message_history[-5:]:
            return False
            
        # Add to history and return True
        self.message_history.append(current_message)
        if len(self.message_history) > 10:
            self.message_history.pop(0)
            
        return True

    def generate_response(self, message):
        """Generate context-aware response using Gemini"""
        try:
            # Build context-aware prompt
            prompt = self.build_prompt(message)
            
            # Generate response
            response = model.generate_content(prompt)
            
            # Process response
            if response and response.text:
                return self.post_process_response(response.text.strip())
            
            return "Sorry, I couldn't generate a response right now."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Oops! Something went wrong."

    def build_prompt(self, message):
        """Construct a detailed, context-aware prompt"""
        # Base personality
        prompt_parts = [
            "You are Muavia, responding to family/friends in a natural Urdu-English mix.",
            "Keep responses casual, short (1-2 lines max), and authentic to how real people chat.",
            "No formalities - respond like you're texting a close friend/family member.",
            "Current conversation context:"
        ]
        
        # Add recent context if available
        if self.conversation_context:
            prompt_parts.extend(self.conversation_context[-3:])
        else:
            prompt_parts.append("[No previous context]")
            
        # Add current message
        prompt_parts.append(f"\n{self.sender_name}: {message}")
        prompt_parts.append("\nMuavia's reply:")
        
        # Add style preferences
        prompt_parts.append(f"\nResponse style: {self.response_style}")
        prompt_parts.append(f"Language preference: {self.language_preference}")
        
        return "\n".join(prompt_parts)

    def post_process_response(self, response):
        """Clean up and enhance the AI response"""
        # Remove any unwanted prefixes
        response = re.sub(r'^(Muavia|Response):\s*', '', response, flags=re.IGNORECASE)
        
        # Ensure proper mixing of Urdu/English based on preference
        if self.language_preference == "urdu":
            response = self.increase_urdu_content(response)
        elif self.language_preference == "english":
            response = self.increase_english_content(response)
            
        # Add occasional emojis for more natural feel
        if random.random() < 0.3:  # 30% chance of adding emoji
            emoji = self.select_appropriate_emoji(response)
            if emoji:
                response = f"{response} {emoji}"
                
        # Ensure proper capitalization
        response = response.capitalize()
        
        return response

    def increase_urdu_content(self, text):
        """Increase Urdu content in response (placeholder for actual implementation)"""
        # In a real implementation, you would have a dictionary of English-to-Urdu translations
        # or use a translation API for common phrases
        return text

    def increase_english_content(self, text):
        """Increase English content in response (placeholder for actual implementation)"""
        return text

    def select_appropriate_emoji(self, text):
        """Select emoji based on message content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['haan', 'yes', 'ok', 'theek']):
            return "👍"
        elif any(word in text_lower for word in ['nahi', 'no', 'not']):
            return "👎"
        elif any(word in text_lower for word in ['thanks', 'shukriya', 'thank you']):
            return "🙏"
        elif any(word in text_lower for word in ['love', 'pyaar', 'miss']):
            return "❤️"
        elif any(word in text_lower for word in ['lol', 'haha', 'funny']):
            return "😂"
        
        return None

    def send_reply(self, reply_text):
        """Send reply with improved reliability"""
        try:
            # Click input box
            self.safe_click(*WHATSAPP_POSITIONS['input_box'])
            time.sleep(0.5)
            
            # Copy reply to clipboard
            pyperclip.copy(reply_text)
            time.sleep(0.5)
            
            # Paste and send
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            
            # Add to conversation context
            self.conversation_context.append(f"Muavia: {reply_text}")
            if len(self.conversation_context) > 5:
                self.conversation_context.pop(0)
                
        except Exception as e:
            print(f"Error sending reply: {e}")

    def analyze_conversation_tone(self, message):
        """Analyze message tone to adjust response style"""
        message_lower = message.lower()
        
        # Check for formal language
        if any(word in message_lower for word in ['please', 'kindly', 'request', 'aap']):
            self.response_style = "slightly_formal"
        # Check for urgent tone
        elif any(word in message_lower for word in ['fast', 'quick', 'urgent', 'jaldi']):
            self.response_style = "concise"
        # Check for casual tone
        elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'kaise ho']):
            self.response_style = "casual"
            
        # Detect language preference
        urdu_words = sum(1 for word in message.split() if self.is_urdu(word))
        english_words = sum(1 for word in message.split() if self.is_english(word))
        
        if urdu_words > english_words * 2:
            self.language_preference = "urdu"
        elif english_words > urdu_words * 2:
            self.language_preference = "english"
        else:
            self.language_preference = "urdu-english"

    def is_urdu(self, word):
        """Check if word contains Urdu characters (basic implementation)"""
        # Urdu Unicode range (approximate)
        urdu_range = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(urdu_range.search(word))

    def is_english(self, word):
        """Check if word is English (basic implementation)"""
        return bool(re.match(r'^[a-zA-Z]+$', word))

    def run(self):
        """Main loop for the auto-replier"""
        print("Auto-replier started. Press Ctrl+C to stop.")
        
        try:
            while True:
                # Get chat history
                chat_log = self.get_chat_history()
                
                # Extract last message
                sender, message = self.extract_last_message(chat_log)
                
                # Check if we should respond
                if (sender and sender == self.sender_name and 
                    message and self.is_new_message(message)):
                    
                    print(f"New message from {sender}: {message}")
                    
                    # Analyze message tone and adjust settings
                    self.analyze_conversation_tone(message)
                    
                    # Generate response
                    response = self.generate_response(message)
                    print(f"Generated response: {response}")
                    
                    # Send reply
                    self.send_reply(response)
                    
                    # Small delay before next check
                    time.sleep(2)
                else:
                    # No new message, wait a bit
                    time.sleep(3)
                    
        except KeyboardInterrupt:
            print("\nAuto-replier stopped.")
        except Exception as e:
            print(f"Error in main loop: {e}")

# Initialize and run the auto-replier
if __name__ == "__main__":
    # Get sender name from user or use default
    sender_name = input("Enter the sender's name to monitor (default: Mama): ").strip() or "Mama"
    
    replier = WhatsAppAutoReplier(sender_name)
    replier.run() 
    