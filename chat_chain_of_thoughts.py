import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# 🔐 Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🧠 Define the system prompt (like role="system" in OpenAI)
system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are: "analyse", "think", "think", "think", "output", "validate", and finally "result".

Rules:
1. Follow the strict JSON output format:
   { "step": "string", "content": "string" }
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query
"""

# 🧠 Create the chat model and start the chat with system prompt
model = genai.GenerativeModel("gemini-2.0-flash-001")  

chat = model.start_chat(history=[
    {"role": "user", "parts": [system_prompt]},
    {"role": "user", "parts": ["What is 3 + 4 * 5?"]},
    {"role": "model", "parts": [json.dumps({"step": "analyse", "content": "The user is asking for an arithmetic operation that involves both addition and multiplication, so I need to follow the order of operations."})]},
    {"role": "model", "parts": [json.dumps({"step": "think", "content": "In order of operations, multiplication should be performed before addition. Therefore, I should first multiply 4 by 5."})]},
    {"role": "model", "parts": [json.dumps({"step": "think", "content": "Calculate the multiplication: 4 * 5 = 20."})]},
    {"role": "model", "parts": [json.dumps({"step": "think", "content": "Next, I need to add the result of the multiplication (20) to the number 3."})]},
])

# 🚀 Continue to next step like assistant would do in OpenAI
response = chat.send_message("Please continue.")
print(response.text)
