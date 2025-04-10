import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash-001")  

# 🔁 Start a chat session to simulate roles
chat = model.start_chat(history=[
    {"role": "user", "parts": ["Hi, who are you?"]},
    {"role": "model", "parts": ["I am a helpful AI assistant created by Google."]},
    {"role": "user", "parts": ["What is greater? 9.8 or 9.11"]}
])

# 🔄 Send next message
response = chat.send_message("Explain why 9.11 is greater.")
print(response.text)
