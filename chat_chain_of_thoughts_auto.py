import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the system-style prompt
system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
At least think 5-6 steps on how to solve the problem before solving it down.

The steps are: "analyse", "think", "output", "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyse the user query.

Output Format:
{ "step": "string", "content": "string" }

Example:
Input: What is 2 + 2.
Output: { "step": "analyse", "content": "Alright! The user is interested in a basic arithmetic operation." }
Output: { "step": "think", "content": "To perform the addition I must go from left to right and add all the operands." }
Output: { "step": "output", "content": "4" }
Output: { "step": "validate", "content": "Seems like 4 is correct answer for 2 + 2." }
Output: { "step": "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers." }
"""

# Helper to strip markdown and get raw JSON
def extract_json(raw_text):
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text[len("```"):].strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()
    return raw_text

# Create the model
model = genai.GenerativeModel("gemini-2.0-flash-001")  

# Start a chat session with system prompt
chat = model.start_chat(history=[
    {"role": "user", "parts": [system_prompt]}
])

# Take user input
query = input("> ")
chat.send_message(query)

# Step-by-step processing
while True:
    response = chat.send_message("Continue the reasoning step by step as per previous rules.")
    
    try:
        raw = extract_json(response.text)
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print("⚠️ Couldn't parse JSON. Raw response:")
        print(response.text)
        break

    step = parsed.get("step")
    content = parsed.get("content")

    if not step or not content:
        print("🚫 Missing 'step' or 'content' key.")
        break

    # Show reasoning steps
    if step != "output":
        print(f"🧠 ({step.upper()}): {content}")
        continue

    # Show final output
    print(f"🤖 FINAL ANSWER: {content}")
    break
