import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your environment variables from .env
load_dotenv()

# Fetch actual key from environment
api_key = os.getenv("GEMINI_API_KEY")

# 🛑 Check if the key was loaded
if not api_key:
    raise ValueError("API key not found. Did you forget to set it in the .env file?")

# Configure the API
genai.configure(api_key=api_key)

# Load the model
model = genai.GenerativeModel("gemini-2.0-flash-001")  # Valid model name

# Generate response
response = model.generate_content("Why is the sky blue?")
print(response.text)


